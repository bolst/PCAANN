@Echo off

start cmd.exe /c run-code && ^
start cmd.exe /c run-web && ^
timeout 6 && ^
start http://localhost:8080