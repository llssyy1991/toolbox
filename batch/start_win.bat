
set filelist="logs/aa_command" "logs/aa_log" "logs/aa_response" "logs/com_log" "logs/er_log" "logs/log_file" "logs/sys_log" "logs/direct_logfile"

call check_file_size.bat "%filelist%"

START /B C:\"Program Files (x86)"\GSSI\SIR30\StartSIR30.exe
:loop
	C:\Users\SIR-30_Admin\Desktop\win_program\windows_code_update\windows_client_test\WindowsClient\out\WindowsClient.exe
	python C:\Users\SIR-30_Admin\Desktop\"program backup 10.20"\"new program"\windows_code_update\windows_client_test\Middleware\error_message.py
	timeout /T 20 /NOBREAK > NUL
	goto :loop