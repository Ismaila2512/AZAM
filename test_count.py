import imaplib, os
from dotenv import load_dotenv
load_dotenv()
m = imaplib.IMAP4_SSL("imap.gmail.com")
m.login(os.environ["GMAIL_USER"], os.environ["GMAIL_PASS"])
m.select("inbox")
stat, msg = m.search(None, '(UNSEEN)')
ids = msg[0].split()
print("UNREAD EMAILS COUNT:", len(ids))
