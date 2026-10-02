# Lo que lanza la tarea programada de Windows.
#
# Un .ps1 y no la tarea llamando a python directamente porque asi hay un
# sitio donde mirar cuando algo falla a las 8 de la manana sin nadie delante.
#
# Registrar / quitar la tarea:  .\tarea.ps1 -Instalar   /  -Quitar

$ErrorActionPreference = 'Stop'
$raiz   = Split-Path -Parent $MyInvocation.MyCommand.Path
$python = "C:\Users\perka\AppData\Local\Programs\Python\Python311\python.exe"
$log    = Join-Path $raiz "datos\pipeline.log"

New-Item -ItemType Directory -Force -Path (Join-Path $raiz "datos") | Out-Null

$env:PYTHONIOENCODING = 'utf-8'
$env:PYTHONUTF8 = '1'

$sello = Get-Date -Format 'yyyy-MM-dd HH:mm:ss'
Add-Content -Path $log -Encoding utf8 -Value "`n========== $sello =========="

Push-Location $raiz
try {
    & $python "pipeline.py" "--escribe" "--push" 2>&1 |
        Tee-Object -FilePath $log -Append
    $codigo = $LASTEXITCODE
} catch {
    Add-Content -Path $log -Encoding utf8 -Value "EXCEPCION: $_"
    $codigo = 1
} finally {
    Pop-Location
}

Add-Content -Path $log -Encoding utf8 -Value "fin (exit $codigo)"

# El log crece un poco cada dia; nos quedamos con lo ultimo.
if ((Get-Item $log).Length -gt 1MB) {
    $t = Get-Content $log -Tail 2000
    Set-Content -Path $log -Value $t -Encoding utf8
}

exit $codigo
