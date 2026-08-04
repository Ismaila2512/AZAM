import os
import imaplib
import email
from email.header import decode_header
import sqlite3
import datetime
import openpyxl
import json
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

GMAIL_USER = os.environ.get("GMAIL_USER")
GMAIL_PASS = os.environ.get("GMAIL_PASS")
GEMINI_KEY = os.environ.get("GEMINI_API_KEY")
NEO_ID = "D0T5M3E2"

client = genai.Client(api_key=GEMINI_KEY)

def init_db():
    conn = sqlite3.connect(os.path.join(os.path.dirname(__file__), "internships.db"))
    c = conn.cursor()
    c.execute("""
    CREATE TABLE IF NOT EXISTS shortlists (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        company_name TEXT,
        next_steps TEXT,
        schedule TEXT,
        email_id TEXT UNIQUE,
        date_received DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)
    conn.commit()
    return conn

def clean_subject(subject):
    if not subject:
        return ""
    decoded_bytes, charset = decode_header(subject)[0]
    if isinstance(decoded_bytes, bytes):
        charset = charset or "utf-8"
        return decoded_bytes.decode(charset, errors="ignore")
    return decoded_bytes

def is_shortlisted(filepath, neoid):
    try:
        wb = openpyxl.load_workbook(filepath, data_only=True)
        for sheet in wb.worksheets:
            for row in sheet.iter_rows(values_only=True):
                for cell in row:
                    if isinstance(cell, str) and neoid.lower() in cell.lower():
                        return True
    except Exception as e:
        print("XLSX parsing error:", e)
    return False

def extract_company_from_subject(subject):
    prompt = f"""
    Extract the company name, scheduled date/time, and the next process step (e.g. PPT, Online Test, Interview) from this CDC email subject.
    Subject: {subject}
    
    Output strictly as JSON:
    {{
        "company_name": "...",
        "schedule": "...",
        "next_steps": "..."
    }}
    """
    try:
        response = client.models.generate_content(
            model='gemini-3.5-flash',
            contents=[prompt],
            config=types.GenerateContentConfig(response_mime_type="application/json")
        )
        return json.loads(response.text)
    except:
        return {"company_name": "Unknown", "schedule": "Unknown", "next_steps": subject}

def draw_background(canvas, doc):
    import math
    from reportlab.lib import colors
    canvas.saveState()
    # Midnight Blue Background (Spider-Man)
    canvas.setFillColor(colors.HexColor('#050A1F'))
    canvas.rect(0, 0, doc.pagesize[0], doc.pagesize[1], fill=1)
    
    # Dark Crimson Red accent top left
    canvas.setFillColor(colors.HexColor('#3a0000'))
    canvas.circle(0, doc.pagesize[1], 280, fill=1, stroke=0)
    
    # Faint Spider Web from top-left
    canvas.setStrokeColor(colors.HexColor('#ffffff'))
    canvas.setLineWidth(0.3)
    cx, cy = 0, doc.pagesize[1]
    for angle in range(0, 91, 15):
        rad = math.radians(angle)
        end_x = cx + 300 * math.cos(rad)
        end_y = cy - 300 * math.sin(rad)
        canvas.line(cx, cy, end_x, end_y)
    
    for r in [60, 120, 180, 240, 300]:
        prev_x, prev_y = None, None
        for angle in range(0, 91, 15):
            rad = math.radians(angle)
            x = cx + r * math.cos(rad)
            y = cy - r * math.sin(rad)
            if prev_x is not None:
                canvas.line(prev_x, prev_y, x, y)
            prev_x, prev_y = x, y

    # Shazam Yellow thunderbolt
    canvas.setStrokeColor(colors.HexColor('#FFD700'))
    canvas.setLineWidth(4)
    bx = doc.pagesize[0] - 60
    by = doc.pagesize[1] - 10
    canvas.line(bx, by, bx - 50, by - 80)
    canvas.line(bx - 50, by - 80, bx + 10, by - 80)
    canvas.line(bx + 10, by - 80, bx - 70, by - 200)
    canvas.restoreState()

def export_shortlist_pdf(rows):
    if not rows:
        return

    from reportlab.lib.pagesizes import letter
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib import colors

    desktop = os.path.join(os.path.expanduser("~"), "Desktop")
    pdf_path = os.path.join(desktop, "AZAM_Shortlists.pdf")
    
    doc = SimpleDocTemplate(pdf_path, pagesize=letter, rightMargin=30, leftMargin=30, topMargin=30, bottomMargin=30)
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'TitleStyle', parent=styles['Heading1'], fontName='Helvetica-BoldOblique',
        fontSize=24, textColor=colors.HexColor('#FFD700'), alignment=1, spaceAfter=30
    )
    
    header_style = ParagraphStyle(
        'Header', parent=styles['Normal'], fontName='Helvetica-BoldOblique',
        fontSize=12, textColor=colors.HexColor('#FFD700'), alignment=1
    )
    
    cell_style = ParagraphStyle(
        'Cell', parent=styles['Normal'], fontName='Helvetica-Bold',
        fontSize=11, textColor=colors.whitesmoke, leading=14
    )
    
    elements = [Paragraph("AZAM! SHORTLIST RADAR", title_style)]
    
    data = [[
        Paragraph("GOLIATH (Company)", header_style),
        Paragraph("NEXT MISSION", header_style),
        Paragraph("DOOMSDAY (Schedule)", header_style)
    ]]
    
    for row in rows:
        comp, steps, sched = row[1], row[2], row[3]
        data.append([
            Paragraph(f"<font color='#ff6666'>{comp}</font>", cell_style),
            Paragraph(str(steps), cell_style),
            Paragraph(str(sched), cell_style)
        ])
        
    t = Table(data, colWidths=[150, 200, 150])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#5D0000')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.HexColor('#FFD700')),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('GRID', (0,0), (-1,-1), 1.5, colors.HexColor('#FFD700')),
        ('BACKGROUND', (0,1), (-1,-1), colors.HexColor('#2A0808')),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.HexColor('#2A0808'), colors.HexColor('#08102A')]),
        ('TOPPADDING', (0,0), (-1,-1), 12), ('BOTTOMPADDING', (0,0), (-1,-1), 12),
        ('LEFTPADDING', (0,0), (-1,-1), 8), ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    
    elements.append(t)
    doc.build(elements, onFirstPage=draw_background, onLaterPages=draw_background)
    print(f"Shortlist PDF generated at {pdf_path}")

def fetch_and_process():
    conn = init_db()
    
    # 1. First, process local Saviynt file if it exists, to test the logic exactly.
    test_xlsx = "/Users/apple/Downloads/saviynt shortlist with role.xlsx"
    test_pdf = "/Users/apple/Downloads/Vellore Institute of Technology Mail - Update _ Saviynt PPT & Online test is scheduled on 04th August 2026 by 2.00pm @Sarojini Naidu Gallery Vellore.pdf"
    
    # Check if we should insert the test data
    c = conn.cursor()
    if os.path.exists(test_xlsx) and os.path.exists(test_pdf):
        c.execute("SELECT id FROM shortlists WHERE company_name='Saviynt'")
        if not c.fetchone():
            if is_shortlisted(test_xlsx, NEO_ID):
                # Extract from test pdf filename
                subj = os.path.basename(test_pdf)
                info = extract_company_from_subject(subj)
                c.execute("INSERT INTO shortlists (company_name, next_steps, schedule, email_id) VALUES (?, ?, ?, ?)",
                          (info.get("company_name", "Saviynt"), info.get("next_steps", "PPT & Online Test"), info.get("schedule", "04th August 2026"), "test_saviynt"))
                conn.commit()
                print("Test Saviynt Shortlist Saved!")
                os.system(f"""osascript -e 'display notification "You are SHORTLISTED for Saviynt! Check AZAM_Shortlists.pdf." with title "AZAM! MATCH"' """)

    # 2. Check IMAP
    try:
        mail = imaplib.IMAP4_SSL("imap.gmail.com")
        mail.login(GMAIL_USER, GMAIL_PASS)
        mail.select("inbox")
        status, messages = mail.search(None, '(UNSEEN FROM "cdc")')
        if messages and messages[0]:
            email_ids = messages[0].split()
            for eid in email_ids:
                res, msg = mail.fetch(eid, "(RFC822)")
                for response_part in msg:
                    if isinstance(response_part, tuple):
                        msg_body = email.message_from_bytes(response_part[1])
                        subject = clean_subject(msg_body["Subject"])
                        
                        xlsxs = []
                        for part in msg_body.walk():
                            if part.get_content_maintype() == "multipart" or part.get("Content-Disposition") is None:
                                continue
                            filename = part.get_filename()
                            if filename and (filename.endswith(".xlsx") or filename.endswith(".xls")):
                                filepath = os.path.join(os.getcwd(), filename)
                                with open(filepath, "wb") as f:
                                    f.write(part.get_payload(decode=True))
                                xlsxs.append(filepath)
                                
                        for xlsx_path in xlsxs:
                            if is_shortlisted(xlsx_path, NEO_ID):
                                info = extract_company_from_subject(subject)
                                try:
                                    c.execute("INSERT INTO shortlists (company_name, next_steps, schedule, email_id) VALUES (?, ?, ?, ?)",
                                            (info.get("company_name", "Unknown"), info.get("next_steps", ""), info.get("schedule", ""), subject))
                                    conn.commit()
                                    comp = info.get("company_name", "Unknown")
                                    os.system(f"""osascript -e 'display notification "You are SHORTLISTED for {comp}! Check AZAM_Shortlists.pdf." with title "AZAM! MATCH"' """)
                                except sqlite3.IntegrityError:
                                    pass # Already recorded
        mail.close()
        mail.logout()
    except Exception as e:
        print("IMAP handling error:", e)

    # 3. Generate PDF if there are records
    c.execute("SELECT * FROM shortlists ORDER BY id DESC")
    rows = c.fetchall()
    if rows:
        export_shortlist_pdf(rows)

if __name__ == "__main__":
    fetch_and_process()
