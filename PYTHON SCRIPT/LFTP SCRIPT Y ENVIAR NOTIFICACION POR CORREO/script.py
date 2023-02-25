import smtplib
from email.mime.text import MIMEText
from subprocess import Popen, PIPE

# FTP LOGIN
HOST = 'sftp://ftp.domain.com'
USER = 'ftpusername'
PASSWORD = 'ftppassword'

# DISTANT DIRECTORY
REMOTE_DIR = '/absolute/path/to/remote/directory'

# LOCAL DIRECTORY
LOCAL_DIR = '/absolute/path/to/local/directory'

# Command to run
cmd = f"""lftp -u "{USER}","{PASSWORD}" {HOST} <<EOF
set sftp:auto-confirm yes
set ssl:verify-certificate no
mirror --use-pget-n=10 {REMOTE_DIR} {LOCAL_DIR}
exit
EOF
"""

# Run the command and get output
process = Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE)
stdout, stderr = process.communicate()

# Check if there were any errors
if stderr:
    print(stderr.decode())
else:
    print(stdout.decode())

# Send email
msg = MIMEText("Transfer finished")
msg["Subject"] = "FTP transfer finished"
msg["From"] = "sender@example.com"
msg["To"] = "recipient@example.com"

s = smtplib.SMTP("smtp.example.com")
s.sendmail("sender@example.com", ["recipient@example.com"], msg.as_string())
s.quit()
