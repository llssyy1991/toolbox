@echo off

set files=%~1

FOR %%A IN (%files%) DO CALL :getFilesize %%A

goto:EOF

:getFilesize

set filesize=%~z1

if %filesize% GEQ 200000000 (
	:: del %~1
	echo deleted
)

echo %filesize%
exit /b