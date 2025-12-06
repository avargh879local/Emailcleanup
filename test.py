import imaplib
import email
import os
from tqdm import tqdm  # Optional for progress
from colorama import Fore, Style, init  # Optional for colors

# Initialize Colorama if available
try:
    init(autoreset=True)
except:
    pass  # Ignore if not installed

# Configuration from env vars
EMAIL_ADDRESS = os.environ.get('EMAIL_ADDRESS')
PASSWORD = os.environ.get('PASSWORD')
IMAP_SERVER = os.environ.get('IMAP_SERVER', 'imap.gmail.com')
DRY_RUN = os.environ.get('DRY_RUN', 'false').lower() == 'true'  # Set to 'true' for preview mode
CRITERIA = os.environ.get('CRITERIA', '(FROM "sender1@example.com"),(X-GM-RAW "category:promotions"),(X-GM-RAW "category:social"),(X-GM-RAW "is:spam")').split(';')  # Semicolon-separated

def hacker_art():
    print(Fore.GREEN + r"""
 _______  __   __  _______  __    _  _______  ___   __    _  _______ 
|       ||  | |  ||       ||  |  | ||       ||   | |  |  | ||       |
|    _  ||  | |  ||    ___||   |_| ||    ___||   | |   |_| ||    ___|
|   |_| ||  |_|  ||   |___ |       ||   |___ |   | |       ||   |___ 
|    ___||       ||    ___||  _    ||    ___||   | |  _    ||    ___|
|   |    |       ||   |___ | | |   ||   |___ |   | | | |   ||   |___ 
|___|    |_______||_______||_|  |__||_______||___| |_|  |__||_______|
    """)

def delete_emails():
    if not EMAIL_ADDRESS or not PASSWORD:
        raise ValueError("EMAIL_ADDRESS and PASSWORD must be set as environment variables.")
    
    hacker_art()
    try:
        mail = imaplib.IMAP4_SSL(IMAP_SERVER)
        mail.login(EMAIL_ADDRESS, PASSWORD)
        mail.select('"[Gmail]/All Mail"')  # Access all emails

        total_deleted = 0
        for criterion in CRITERIA:
            criterion = criterion.strip()
            typ, data = mail.uid('SEARCH', None, criterion)
            if data[0]:
                email_ids = [uid.decode() for uid in data[0].split()]
                total_deleted += len(email_ids)
                desc = "Previewing" if DRY_RUN else "Deleting"
                for num in tqdm(email_ids, desc=f"{desc} emails for {criterion}", unit="email"):
                    # Fetch headers for logging (optional; skip for speed)
                    typ, msg_data = mail.uid('FETCH', num, '(RFC822.HEADER)')
                    if msg_data[0] is not None:
                        msg = email.message_from_bytes(msg_data[0][1])
                        sender = msg['from']
                        subject = msg['subject']
                        print(Fore.GREEN + f"{'Would delete' if DRY_RUN else 'Deleting'} email from {sender}: '{subject}'")
                    
                    if not DRY_RUN:
                        mail.uid('STORE', num, '+FLAGS', '(\\Deleted)')

        if not DRY_RUN:
            mail.expunge()
        mail.logout()

        action = "would be deleted" if DRY_RUN else "deleted"
        print(Fore.YELLOW + f'{total_deleted} emails {action} successfully!')

    except Exception as e:
        print(Fore.RED + "Error occurred:", e)
        raise

# Run the script
delete_emails()
