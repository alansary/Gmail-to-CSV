"""
Exports Gmail inbox to CSV

1. Enable IMAP in your Gmail settings
- Log on to your Gmail account and go to Settings
- See All Settings
- Select "Forwarding and POP/IMAP" tab
- In the "IMAP access" section
- Select Enable IMAP

2. If you have 2-factor authentication, Gmail requires you to create an application
specific password that you need to use. 
- Go to your Google account settings and click on 'Security'
- Scroll down to App Passwords under 2 step verification
- Select Mail under Select App. and Other under Select Device. (Give a name, e.g., Python)
- The system gives you a password that you need to use to authenticate from Python
"""

import imaplib
import email
import yaml
import csv

# Load the user and password from yaml file
with open("credentials.yml") as f:
    content = f.read()

credentials = yaml.load(content, Loader=yaml.FullLoader)
user, password = credentials["user"], credentials["password"]

# URL for IMAP connection
imap_url = "imap.gmail.com"

# Connection with GMAIL using SSL
my_mail = imaplib.IMAP4_SSL(imap_url, 993)

# Log in using your credentials
my_mail.login(user, password)

# Select the Inbox to fetch messages
status, messages_count = my_mail.select("Inbox")

if status != "OK":
    exit("Incorrect mail box")

messages = []
for i in range(1, int(messages_count[0])):
    res, msg = my_mail.fetch(str(i), "(RFC822)")
    for response in msg:
        if isinstance(response, tuple):
            my_msg = email.message_from_bytes(response[1])
            # print("_________________________________________")
            message_subject = my_msg["subject"].replace("|", "")
            message_from = my_msg["from"].replace("|", "")
            # print("subj:", message_subject)
            # print("from:", message_from)
            # print("body:")
            body = ""
            for part in my_msg.walk():
                # print(part.get_content_type())
                if part.get_content_type() == "text/plain":
                    # print(part.get_payload())
                    body += part.get_payload()
            body = body.replace("|", "")
            # print(body)
            message = {
                "subject": message_subject,
                "from": message_from,
                "body": body,
            }
            messages.append(message)
    print(f"Fetched message #{i}")

messages_file = open("messages.csv", "w")
messages_writer = csv.writer(messages_file, delimiter ='|')
messages_writer.writerow(["subject", "from", "body"])
for message in messages:
    messages_writer.writerow(message.values())
messages_file.close()

exit()