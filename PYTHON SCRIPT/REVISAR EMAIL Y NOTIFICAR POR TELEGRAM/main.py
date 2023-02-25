import mailbot
import time

chatId       = 'ID'
tgApiToken   = 'TOKEN'
mailServer   = 'SERVER'
mailAddress  = 'CORREO'
mailPassword = 'PASS'
mailFolder   = 'Inbox'

mailbox = mailbot.Mailbox(mailServer, mailAddress, mailPassword, mailFolder)
sender  = mailbot.TgSender(tgApiToken, chatId)

print('Start checking..')
while(1):
  emails = mailbox.getUnseenMails(False)

  for email in emails:
    print(email)
    data = str(email['sender']) + '\n\n' + str(email['subject'])
    sender.send(data)

  time.sleep(30)
    
    
