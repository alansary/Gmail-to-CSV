"""
Exports Gmail inbox to CSV
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

# Load the key and value from yaml file
with open("config.yml") as f:
    content = f.read()

config = yaml.load(content, Loader=yaml.FullLoader)
key, value = config['key'], config['value']

# Search for emails with specific key and value
_, data = my_mail.search(None, key, value)

# IDs of all emails that we want to fetch 
mail_id_list = data[0].split()

# Empty list to capture all messages
msgs = []
# Iterate through messages and extract data into the msgs list
for num in mail_id_list:
    typ, data = my_mail.fetch(num, '(RFC822)') # RFC822 returns whole message (BODY fetches just body)
    msgs.append(data)

messages = []
for i, msg in enumerate(msgs[::-1]):
    for response_part in msg:
        if type(response_part) is tuple:
            my_msg=email.message_from_bytes((response_part[1]))
            # print("_________________________________________")
            message_subject = my_msg["subject"].replace("|", "")
            message_from = my_msg["from"].replace("|", "")
            # print("subj:", message_subject)
            # print("from:", message_from)
            # print("body:")
            body = ""
            for part in my_msg.walk():  
                #print(part.get_content_type())
                if part.get_content_type() == 'text/plain':
                    # print(part.get_payload())
                    body += part.get_payload()
            body = body.replace("|", "")
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