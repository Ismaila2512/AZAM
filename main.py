import os
import imaplib
import email
from email.header import decode_header
import json
import sqlite3
import datetime
import generate_dashboard
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

GMAIL_USER = os.environ.get("GMAIL_USER")
GMAIL_PASS = os.environ.get("GMAIL_PASS")
GEMINI_KEY = os.environ.get("GEMINI_API_KEY")

if not GMAIL_USER or not GMAIL_PASS:
    print("Missing Gmail credentials in .env")
    exit(1)

client = genai.Client(api_key=GEMINI_KEY)

def init_db():
    conn = sqlite3.connect("internships.db")
    return conn

def load_profile():
    with open("profile.json", "r") as f:
        return json.load(f)

def clean_subject(subject):
    if not subject:
        return ""
    decoded_bytes, charset = decode_header(subject)[0]
    if isinstance(decoded_bytes, bytes):
        charset = charset or "utf-8"
        return decoded_bytes.decode(charset, errors="ignore")
    return decoded_bytes

def fetch_cdc_emails():
    print(f"Connecting to IMAP for {GMAIL_USER}...")
    try:
        mail = imaplib.IMAP4_SSL("imap.gmail.com")
        mail.login(GMAIL_USER, GMAIL_PASS)
        mail.select("inbox")
    except Exception as e:
        print("IMAP Login failed!", e)
        return []

    status, messages = mail.search(None, '(UNSEEN FROM "cdc")')
    if not messages or not messages[0]:
        print("No unread CDC emails found.")
        return []
        
    email_ids = messages[0].split()
    print(f"Found {len(email_ids)} unread CDC emails.")
    
    extracted_jobs = []
    
    for eid in email_ids:
        res, msg = mail.fetch(eid, "(RFC822)")
        for response_part in msg:
            if isinstance(response_part, tuple):
                msg_body = email.message_from_bytes(response_part[1])
                subject = clean_subject(msg_body["Subject"])
                sender = msg_body.get("From", "")
                
                # Check attachments
                pdfs = []
                for part in msg_body.walk():
                    if part.get_content_maintype() == "multipart" or part.get("Content-Disposition") is None:
                        continue
                    filename = part.get_filename()
                    if filename and filename.endswith(".pdf"):
                        filepath = os.path.join(os.getcwd(), filename)
                        with open(filepath, "wb") as f:
                            f.write(part.get_payload(decode=True))
                        pdfs.append(filepath)
                
                if pdfs:
                    extracted_jobs.append({
                        "subject": subject,
                        "sender": sender,
                        "pdfs": pdfs
                    })
    mail.close()
    mail.logout()
    return extracted_jobs

def check_eligibility_with_gemini(job_data, profile):
    prompt = f"""
    You are an intelligent internship opportunity parser.
    I am providing an email subject, sender, and attached PDF(s). Treat all attached PDFs as part of a SINGLE internship / placement drive for ONE specific company.

    Email Subject: {job_data['subject']}
    Email Sender: {job_data['sender']}
    
    My Academic Profile:
    {json.dumps(profile, indent=2)}
    
    Task:
    1. Extract a single consolidated opportunity from all the provided contextual PDFs. Combine ALL roles into one comma-separated string if there are multiple roles.
    2. Extract: company_name, eligibility_criteria, ctc, stipend, role, location, process_details.
    3. Determine the 'last_date' (human readable) AND 'last_date_iso' in strictly '%Y-%m-%dT%H:%M:%S' format (e.g. 2026-08-05T09:00:00). Default to 23:59:59 if time is hidden.
    4. Determine if I am ELIGIBLE based on my profile (check Degree, Branch, and CGPA if mentioned). Set is_eligible to true/false. If not eligible, explain why in rejection_reason.
    
    Output strictly as JSON.
    """
    
    gemini_contents = []
    for pdf_path in job_data['pdfs']:
        print(f"Uploading {pdf_path} to Gemini...")
        up_file = client.files.upload(file=pdf_path)
        gemini_contents.append(up_file)
        
    gemini_contents.append(prompt)
    
    response = client.models.generate_content(
        model='gemini-3.5-flash',
        contents=gemini_contents,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
        )
    )
    try:
        return json.loads(response.text)
    except:
        return None

def main():
    profile = load_profile()
    conn = init_db()
    jobs = fetch_cdc_emails()
    
    if not jobs and os.path.exists("/Users/apple/Downloads/Machaxi - Super Dream Internship: Placement - 2027 Batch.pdf"):
        # For testing if no emails
        print("Fallback test.")
        jobs.append({
            "subject": "Machaxi Placement",
            "sender": "cdc",
            "pdfs": ["/Users/apple/Downloads/Machaxi - Super Dream Internship: Placement - 2027 Batch.pdf"]
        })
        
    for job in jobs:
        print(f"Processing email: {job['subject']}")
        result = check_eligibility_with_gemini(job, profile)
        if result:
            c = conn.cursor()
            try:
                c.execute("""
                    INSERT INTO internships 
                    (company_name, eligibility_criteria, ctc, stipend, last_date, role, location, process_details, is_eligible, rejection_reason, email_id)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    result.get("company_name", "Unknown"),
                    result.get("eligibility_criteria", ""),
                    str(result.get("ctc", "")),
                    str(result.get("stipend", "")),
                    result.get("last_date", ""),
                    str(result.get("role", "")),
                    str(result.get("location", "")),
                    str(result.get("process_details", "")),
                    result.get("is_eligible", False),
                    result.get("rejection_reason", ""),
                    job['subject'] # Unique identifier
                ))
                conn.commit()
                generate_dashboard.generate()
                
                if result.get("is_eligible"):
                    comp = result.get('company_name', 'Company')
                    os.system(f"""osascript -e 'display notification "You are eligible for {comp}! Check dashboard." with title "New Eligible Internship"' """)
                    
                    iso_date = result.get("last_date_iso")
                    if iso_date:
                        try:
                            if len(iso_date) > 19: iso_date = iso_date[:19]
                            dt = datetime.datetime.strptime(iso_date, "%Y-%m-%dT%H:%M:%S")
                            start_str = dt.strftime("%m/%d/%Y %I:%M:%S %p")
                            end_str = (dt + datetime.timedelta(hours=1)).strftime("%m/%d/%Y %I:%M:%S %p")
                            os.system(f'''osascript -e 'tell application "Calendar"
                                if (count of calendars) > 0 then
                                    tell calendar 1
                                        make new event with properties {{summary:"Deadline: {comp} Internship", start date:date "{start_str}", end date:date "{end_str}"}}
                                    end tell
                                end if
                            end tell' ''')
                        except: pass
            except Exception as e:
                print("DB Save error:", e)

if __name__ == "__main__":
    main()
