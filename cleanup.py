import imaplib
import email
import os
from tqdm import tqdm

# Config from secrets
EMAIL = os.environ["EMAIL_ADDRESS"]
PASS = os.environ["PASSWORD"]
DRY_RUN = os.environ.get("DRY_RUN", "true").lower() == "true"
RAW_CRITERIA = os.environ.get("CRITERIA", 'X-GM-RAW "category:promotions"').split(";")

def banner():
    print("\n" + "═" * 60)
    print("       EMAIL CLEANUP BOT IS NOW ACTIVE")
    print("═" * 60 + "\n")

def main():
    banner()
    mail = imaplib.IMAP4_SSL("imap.gmail.com")
    mail.login(EMAIL, PASS)
    mail.select('"[Gmail]/All Mail"')

    total = 0
    for crit in RAW_CRITERIA:
        crit = crit.strip()
        if not crit:
            continue
        print(f"Searching → {crit}")
        typ, data = mail.uid("SEARCH", None, crit)
        if not data[0]:
            print("  → 0 emails found\n")
            continue

        uids = data[0].split()
        total += len(uids)
        action = "Would delete" if DRY_RUN else "DELETING"

        for uid in tqdm(uids, desc=action, unit="email"):
            if not DRY_RUN:
                mail.uid("STORE", uid, "+FLAGS", "(\\Deleted)")

            # Optional: show what we're deleting (safe even in dry-run)
            typ, msg_data = mail.uid("FETCH", uid, "(RFC822.HEADER)")
            if msg_data[0]:
                header = email.message_from_bytes(msg_data[0][1])
                sender = header.get("From", "Unknown")
                subject = header.get("Subject", "No Subject")
                print(f"  → {sender[:40]:<40} | {subject[:50]}")

    if not DRY_RUN:
        mail.expunge()
        print(f"\nDELETED {total} emails permanently!")
    else:
        print(f"\nDRY RUN: {total} emails would be deleted (safe mode)")

    mail.close()
    mail.logout()

if __name__ == "__main__":
    main()
