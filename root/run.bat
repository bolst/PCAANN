@Echo off

cmd /c start /min cmd /k run-code && ^
cmd /c start /min cmd /k run-web && ^
timeout 5 && ^
start http://localhost:8080