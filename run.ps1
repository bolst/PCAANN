Start-Process Powershell { .\run-code.ps1 }
Start-Process Powershell { .\run-web.ps1 }
Start-Sleep -Seconds 6
Start-Process "http://localhost:8080"