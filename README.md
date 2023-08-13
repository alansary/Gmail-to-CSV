# Gmail to CSV 🤗

### Enable IMAP in your Gmail Settings:
    - Log on to your Gmail account and go to Settings
    - See All Settings
    - Select "Forwarding and POP/IMAP" tab
    - In the "IMAP access" section
    - Select Enable IMAP

### If you have 2-factor authentication, Gmail requires you to create an application specific password that you need to use
    - Go to your Google account settings and click on 'Security'
    - Scroll down to App Passwords under 2 step verification
    - Select Mail under Select App. and Other under Select Device. (Give a name, e.g., Python)
    - The system gives you a password that you need to use to authenticate from Python


### Update credentials.yml file
    - Enter your email
    - Enter your password


### Extract all emails
```bash
python3 extract.py
```

### Extract emails with filter
    - Enter the key and value in config.yml

```bash
python3 extract-with-filter.py
```