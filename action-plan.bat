@echo off

call "./.venv/Scripts/activate.bat"

:: Search for config.json in the current directory
for /r %%i in (config.json) do (
    set "config=%%i"
    goto :found
)

:found
:: Check if config.json was found
if "%config%"=="" (
    echo Config file "config.json" was not found in the current directory or its subdirectories.
    pause
    exit /b
)

:: Promot for application name
set /p "application_name=Enter application name: "

echo Application name: %application_name%
echo .
echo .
echo .

python -m cast_action_plan.main -a %application_name% -c %config%

echo the end of the script
echo .
echo .
echo .
pause

:: End of the script