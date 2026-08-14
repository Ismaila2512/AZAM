import sqlite3
import os
import math
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

def draw_background(canvas, doc):
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
    # Radiating threads
    cx, cy = 0, doc.pagesize[1]
    for angle in range(0, 91, 15):
        rad = math.radians(angle)
        end_x = cx + 300 * math.cos(rad)
        end_y = cy - 300 * math.sin(rad)
        canvas.line(cx, cy, end_x, end_y)
    
    # Arching connecting webs (simplified using lines to avoid complex arc math)
    for r in [60, 120, 180, 240, 300]:
        prev_x, prev_y = None, None
        for angle in range(0, 91, 15):
            rad = math.radians(angle)
            x = cx + r * math.cos(rad)
            y = cy - r * math.sin(rad)
            if prev_x is not None:
                # Add slight sag to web
                canvas.line(prev_x, prev_y, x, y)
            prev_x, prev_y = x, y

    # Shazam Yellow thunderbolt abstract accent top right
    canvas.setStrokeColor(colors.HexColor('#FFD700'))
    canvas.setLineWidth(4)
    bolt_x = doc.pagesize[0] - 60
    bolt_y = doc.pagesize[1] - 10
    canvas.line(bolt_x, bolt_y, bolt_x - 50, bolt_y - 80)
    canvas.line(bolt_x - 50, bolt_y - 80, bolt_x + 10, bolt_y - 80)
    canvas.line(bolt_x + 10, bolt_y - 80, bolt_x - 70, bolt_y - 200)

    canvas.restoreState()

def generate_pdf():
    conn = sqlite3.connect(os.path.join(os.path.dirname(__file__), "internships.db"))
    c = conn.cursor()
    c.execute("SELECT company_name, role, ctc, stipend, last_date, location, process_details FROM internships WHERE is_eligible = 1 ORDER BY id DESC")
    rows = c.fetchall()
    
    if not rows:
        print("No eligible internships found.")
        return

    desktop = os.path.join(os.path.expanduser("~"), "Desktop")
    pdf_path = os.path.join(desktop, "Eligible_Internships.pdf")
    
    doc = SimpleDocTemplate(
        pdf_path, 
        pagesize=letter,
        rightMargin=30, leftMargin=30,
        topMargin=30, bottomMargin=30
    )
    
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'TitleStyle',
        parent=styles['Heading1'],
        fontName='Helvetica-BoldOblique',
        fontSize=24,
        textColor=colors.HexColor('#FFD700'),
        alignment=1,
        spaceAfter=30
    )
    
    header_style = ParagraphStyle(
        'Header',
        parent=styles['Normal'],
        fontName='Helvetica-BoldOblique',
        fontSize=11,
        textColor=colors.HexColor('#FFD700'),
        alignment=1
    )
    
    cell_style = ParagraphStyle(
        'Cell',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10,
        textColor=colors.whitesmoke,
        leading=14
    )
    
    elements = []
    elements.append(Paragraph("AZAM! RADAR", title_style))
    
    data = [[
        Paragraph("GOLIATH", header_style),
        Paragraph("MISSION", header_style),
        Paragraph("POWER LEVEL", header_style),
        Paragraph("DOOMSDAY", header_style),
        Paragraph("GROUND ZERO", header_style)
    ]]
    
    for row in rows:
        company = str(row[0]) if row[0] else "UNKNOWN"
        role = str(row[1]) if row[1] else "CLASSIFIED"
        ctc = str(row[2]) if row[2] else "TBD"
        stipend = str(row[3]) if row[3] else "TBD"
        last_date = str(row[4]).split('T')[0] if row[4] else "TBD"
        location = str(row[5]) if row[5] else "GLOBAL"
        
        ctc_block = f"<font color='#ffffff'>CTC:</font> {ctc}<br/><font color='#aaaaaa'>Stipend:</font> {stipend}"
        
        data.append([
            Paragraph(f"<font color='#ff6666'>{company}</font>", cell_style),
            Paragraph(role, cell_style),
            Paragraph(ctc_block, cell_style),
            Paragraph(last_date, cell_style),
            Paragraph(location, cell_style)
        ])
        
    t = Table(data, colWidths=[110, 130, 110, 90, 100])
    
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#5D0000')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.HexColor('#FFD700')),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        
        # Golden glowing borders
        ('GRID', (0,0), (-1,-1), 1.5, colors.HexColor('#FFD700')),
        
        # Alternating Crimson and Deep Blue rows
        ('BACKGROUND', (0,1), (-1,-1), colors.HexColor('#2A0808')),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.HexColor('#2A0808'), colors.HexColor('#08102A')]),
        
        ('TOPPADDING', (0,0), (-1,-1), 12),
        ('BOTTOMPADDING', (0,0), (-1,-1), 12),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    
    elements.append(t)
    doc.build(elements, onFirstPage=draw_background, onLaterPages=draw_background)
    print(f"PDF successfully generated at {pdf_path}")

if __name__ == "__main__":
    generate_pdf()
