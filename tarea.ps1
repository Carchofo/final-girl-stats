# Registra (o quita) la tarea programada que corre el pipeline.
#
#   .\tarea.ps1 -Instalar     una vez al dia a las 08:30
#   .\tarea.ps1 -Estado
#   .\tarea.ps1 -Ahora        lanza una pasada y no espera
#   .\tarea.ps1 -Quitar
#
# No hace falta ser admin: la tarea es del usuario. Tampoco despierta el
# equipo: si el PC esta apagado a las 08:30, corre cuando arranque.

param(
    [switch]$Instalar,
    [switch]$Quitar,
    [switch]$Estado,
    [switch]$Ahora,
    [string]$Hora = "08:30"
)

$nombre = "FinalGirl-Pipeline"
$raiz   = Split-Path -Parent $MyInvocation.MyCommand.Path
$script = Join-Path $raiz "ejecutar.ps1"

if ($Instalar) {
    $accion = New-ScheduledTaskAction `
        -Execute "powershell.exe" `
        -Argument "-NoProfile -NonInteractive -ExecutionPolicy Bypass -File `"$script`"" `
        -WorkingDirectory $raiz

    $disparo = New-ScheduledTaskTrigger -Daily -At $Hora

    # StartWhenAvailable: si el PC estaba apagado, se recupera la pasada.
    # No DontStopIfGoingOnBatteries porque esto es un sobremesa.
    $opciones = New-ScheduledTaskSettingsSet `
        -StartWhenAvailable `
        -AllowStartIfOnBatteries `
        -ExecutionTimeLimit (New-TimeSpan -Hours 1) `
        -MultipleInstances IgnoreNew

    Register-ScheduledTask -TaskName $nombre -Action $accion -Trigger $disparo `
        -Settings $opciones -Description "Final Girl: hoja -> datos -> rama pc/datos" `
        -Force | Out-Null

    Write-Host "Tarea '$nombre' registrada, diaria a las $Hora."
    Write-Host "Log: $(Join-Path $raiz 'datos\pipeline.log')"
}

if ($Quitar) {
    Unregister-ScheduledTask -TaskName $nombre -Confirm:$false
    Write-Host "Tarea '$nombre' eliminada."
}

if ($Ahora) {
    Start-ScheduledTask -TaskName $nombre
    Write-Host "Lanzada. Mira el log en datos\pipeline.log"
}

if ($Estado -or (-not ($Instalar -or $Quitar -or $Ahora))) {
    $t = Get-ScheduledTask -TaskName $nombre -ErrorAction SilentlyContinue
    if (-not $t) { Write-Host "No registrada. Usa: .\tarea.ps1 -Instalar"; return }
    $i = Get-ScheduledTaskInfo -TaskName $nombre
    Write-Host "Tarea:    $nombre  [$($t.State)]"
    Write-Host "Anterior: $($i.LastRunTime)  resultado $($i.LastTaskResult)"
    Write-Host "Siguiente:$($i.NextRunTime)"
}
