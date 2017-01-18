import subprocess

def command_no_popout(command):
    startupinfo = subprocess.STARTUPINFO()
    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    return subprocess.call(command , startupinfo=startupinfo )

def command_output_NoPopout(command):
    startupinfo = subprocess.STARTUPINFO()
    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    try:
        check = subprocess.check_output(command, startupinfo=startupinfo)
        return check

    except subprocess.CalledProcessError, e:
        return 1
