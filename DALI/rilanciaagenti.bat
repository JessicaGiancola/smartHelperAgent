@echo off
cls
title "MAS"
set sicstus_home=C:\Program Files\SICStus Prolog VC16 4.6.0\bin
::set main_home=%~dp0\..
set main_home=.
set dali_home=src
set conf_dir=conf
set prolog=%sicstus_home%\spwin.exe
set daliH=%dali_home:\=/%
set WAIT=ping -n 6 127.0.0.1

del /q work\*.pl
copy mas\*.txt work

FOR /F "tokens=*" %%G IN ('dir /b mas\*.txt') DO (
@echo agente: %%~nG
call conf/makeconf %%~nG %%G
call conf/startagent %%G "%prolog%" "%dali_home%"
%WAIT% >nul
)