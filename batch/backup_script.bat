
SET Source_directory="C:\Users\SIR-30_Admin\Desktop\backup folder"
SET Remote_target="\\192.168.1.17\backup folder"
SET dropbox_directory="C:\Users\SIR-30_Admin\Dropbox (Infratek)\Infratek Team Folder\backup folder"
SET wiki_folder="C:\xampp\htdocs\mediawiki"
SET wiki_backup="C:\Users\SIR-30_Admin\Desktop\backup folder\media_wiki"

robocopy %wiki_folder% %wiki_backup% /XO /FFT /E
robocopy %Source_directory% %Remote_target% /XO /FFT /E
robocopy %Source_directory% %dropbox_directory% /XO /FFT /E