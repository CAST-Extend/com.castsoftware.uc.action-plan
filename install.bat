@echo off

set local=%cd%
set venv_loc=%local%/.venv

if NOT exist %venv_loc% (
    py -m venv %venv_loc%
)

if exist %venv_loc% (
    echo Creating new venv
    call %venv_loc%\scripts\activate
    call pip install com.castsoftware.uc.action-plan==1.0.0 --upgrade 
) else (
    echo Error initializing virtual enviroment (%venv_loc%)    
    exit /b 1000
)


