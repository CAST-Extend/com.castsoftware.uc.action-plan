@@echo off

set application_name=%1
set config=%2

IF NOT EXIST %config% (
  Echo Config file does not exist 
  exit /b 1
)

call .\.venv\scripts\activate

python -m cast_action_plan.main -a %application_name% -c %config% 

exit /b

:error

