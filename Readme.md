Title: Gmail Email Deletion Script
//
**Requirements**
//
* **Python 3:** You'll need Python 3 installed on your system. Download the latest version from [https://www.python.org/downloads/](https://www.python.org/downloads/)
* **Dependencies:** Install the required libraries using pip:
    ```bash
    pip install imaplib email
    ```

**Configuration**

1. **Copy and paste the code below into this file.**
2. **Gmail Credentials:** Replace the placeholder values within the code with your own details:
    ```python
    EMAIL_ADDRESS = 'your_email@gmail.com'  
    PASSWORD = 'your_app_password'  
    ```
3. **App Password:**  Make sure you've created an app password in your Gmail security settings. See these instructions: [https://support.google.com/accounts/answer/185833](https://support.google.com/accounts/answer/185833)
4. **Message IDs:** Replace the placeholder message IDs with the actual IDs of the emails you want to delete:
    ```python
    MESSAGE_IDS = ['<message_id_1@gmail.com>', '<message_id_2@gmail.com>', ...]
    ```

**How to Find Message IDs in Gmail**

1.  Open the specific email you want to delete.
2.  Click the three dots in the top right corner.
3.  Select "Show Original".
4.  Find the `Message-ID` header (e.g., `<some_unique_id@gmail.com>`).

**Python Code**

```python
import imaplib
import email

# Configuration
EMAIL_ADDRESS = 'your_email@gmail.com'  
PASSWORD = 'your_app_password'  
IMAP_SERVER = 'imap.gmail.com' 

# Message IDs of the emails to delete 
MESSAGE_IDS = ['<message_id_1@gmail.com>', '<message_id_2@gmail.com>', ...]  

def delete_emails():
    try:
        mail = imaplib.IMAP4_SSL(IMAP_SERVER)
        mail.login(EMAIL_ADDRESS, PASSWORD)
        mail.select('inbox')

        message_id_str = ','.join(MESSAGE_IDS) 
        typ, data = mail.uid('SEARCH', None, 'UID ' + message_id_str) 

        if data[0] != '':
            for num in data[0].split():
                mail.store(num, '+FLAGS', '\\Deleted')

        mail.expunge()
        mail.close()
        mail.logout()

        print('Emails deleted successfully!')

    except Exception as e:
        print("Error occurred:", e)

# Run the deletion process
delete_emails()

