@Echo off

REM this will stop all open command prompts and stop the running docker container
docker container stop pca_ann_container
docker container rm pca_ann_container
taskkill /f /im python3.10.exe
taskkill /f /im cmd.exe