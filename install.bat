@echo off
setlocal enabledelayedexpansion

:: Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python is not installed.
    echo Please install Python and add it to the system path and rerun this installation script.
    exit /b 1000
)

:: Check if Python is in the system PATH
where python >nul 2>&1
if %errorlevel% neq 0 (
    echo Python is not found in the system PATH.
    exit /b 1000
)

:AskDestination
echo Please provide the destination folder:
set /p destinationFolder=Destination: 

if not exist "%destinationFolder%" (
    echo The provided directory does not exist. Please provide a valid directory.
    goto AskDestination
)

cd /d "%destinationFolder%"

echo Installing in %destinationFolder%...

:: Set the path to the ".venv" folder in the same directory
set "venv_loc=%destinationFolder%\.venv"

:: Check if .venv is set up
if NOT exist "%venv_loc%" (
    pushd "%destinationFolder%"
    py -m venv "%venv_loc%"
    popd
)

:: Copying files from the directory where install.bat is located to the destination folder
copy /Y "%~dp0action-plan.bat" "%destinationFolder%\action-plan.bat"
copy /Y "%~dp0install.bat" "%destinationFolder%\install.bat"
copy /Y "%~dp0config.json" "%destinationFolder%\config.json"

:: Activate virtual environment
call "%destinationFolder%\.venv\Scripts\activate.bat"
pip install com.castsoftware.uc.action-plan==1.0.0

call.\action-plan.bat
:end