import imaplib
import os
from dotenv import load_dotenv
load_dotenv()
try:
    m = imaplib.IMAP4_SSL("imap.gmail.com")
    m.login(os.environ["GMAIL_USER"], os.environ["GMAIL_PASS"])
    print("IMAP SUCCESS")
    m.logout()
except Exception as e:
    print("IMAP FAILED:", e)
