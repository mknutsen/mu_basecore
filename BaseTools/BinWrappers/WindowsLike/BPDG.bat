<<<<<<< HEAD
@setlocal
@set ToolName=%~n0%
@set PYTHONPATH=%PYTHONPATH%;%BASE_TOOLS_PATH%\Source\Python
@%PYTHON_HOME%\python.exe -m %ToolName%.%ToolName% %*
=======
@setlocal
@set ToolName=%~n0%
@set PYTHONPATH=%PYTHONPATH%;%BASE_TOOLS_PATH%\Source\Python
@"%PYTHON3%" -m %ToolName%.%ToolName% %*
>>>>>>> moving mu_build 1808 in HEAD=7f6adb264392130c1b9aa01b8796fa9fdf87b66f
