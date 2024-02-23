import imaplib
from tqdm import tqdm
# Configuration
EMAIL_ADDRESS = 'Put _your_email_here'  
PASSWORD = 'App_password'  # For Gmail, use an app password
IMAP_SERVER = 'imap.gmail.com' 

## Email addresses of the senders whose emails to delete
SENDER_EMAILS = ['newsletter@newsbreakexpress.com']  # Replace with actual sender email addresses

def delete_emails():
    while True:
        try:
            mail = imaplib.IMAP4_SSL(IMAP_SERVER)
            mail.login(EMAIL_ADDRESS, PASSWORD)
            mail.select('inbox')

            total_deleted = 0
            for sender_email in SENDER_EMAILS:
                typ, data = mail.uid('SEARCH', None, '(FROM "' + sender_email + '")')
                if data[0]:
                    email_ids = data[0].split()
                    total_deleted += len(email_ids)
                    for num in tqdm(email_ids, desc="Deleting emails", unit="email"):
                        mail.uid('STORE', num, '+FLAGS', '(\\Deleted)')

            mail.expunge()
            mail.close()
            mail.logout()

            if total_deleted == 0:
                break

            print(str(total_deleted) + ' emails deleted successfully!')

        except Exception as e:
            print("Error occurred:", e)
            break

# Example usage
delete_emails()