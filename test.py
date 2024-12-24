import imaplib
import email
from tqdm import tqdm
from colorama import Fore, Style, init

# Initialize Colorama
init(autoreset=True)

# Configuration
EMAIL_ADDRESS = 'abyvarghese2007@gmail.com'
PASSWORD = 'your app password here'  # For Gmail, use an app password
IMAP_SERVER = 'imap.gmail.com'

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
    hacker_art()
    try:
        mail = imaplib.IMAP4_SSL(IMAP_SERVER)
        mail.login(EMAIL_ADDRESS, PASSWORD)
        mail.select('"[Gmail]/All Mail"')  # Selects all mail across categories

        criteria = [
            '(FROM "sender1@example.com")',  # Add your specific senders or criteria here
            '(X-GM-RAW "category:promotions")',
            '(X-GM-RAW "category:social")',
            '(X-GM-RAW "is:spam")'
        ]

        total_deleted = 0
        for criterion in criteria:
            typ, data = mail.uid('SEARCH', None, criterion)
            if data[0]:
                email_ids = data[0].split()
                total_deleted += len(email_ids)
                for num in tqdm(email_ids, desc="Deleting emails", unit="email"):
                    # Fetch the email's headers
                    typ, msg_data = mail.uid('FETCH', num, '(RFC822.HEADER)')
                    if msg_data[0] is not None:
                        msg = email.message_from_bytes(msg_data[0][1])
                        sender = msg['from']
                        subject = msg['subject']
                        print(Fore.GREEN + f"Deleting email from {sender}: '{subject}'")
                    
                    # Mark the email for deletion
                    mail.uid('STORE', num, '+FLAGS', '(\\Deleted)')

        mail.expunge()
        mail.logout()

        print(Fore.YELLOW + f'{total_deleted} emails deleted successfully!')

    except Exception as e:
        print(Fore.RED + "Error occurred:", e)

# Example usage
delete_emails()
