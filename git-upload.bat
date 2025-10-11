@echo off
chcp 65001
echo.
echo INICIANDO UPLOAD PARA GIT...
echo.
git add .
git commit -m "update %date% %time%"
git pull origin main
git push origin main
echo.
echo UPLOAD CONCLUIDO!
echo.
pause