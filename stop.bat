@Echo off

REM this will stop all open command prompts and stop the running docker image
docker stop pca_ann_image && ^
taskkill /f /im OpenConsole.exe