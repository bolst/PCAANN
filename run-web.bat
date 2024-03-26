@Echo off

REM for development, change to "condition=dev"
REM for production, change to "condition="
set "condition="

if defined condition (dotnet watch --project PCAANN\PCAANN\PCAANN.csproj) else (call run-docker)