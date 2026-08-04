import re

with open("shortlist_bot.py", "r") as f:
    text = f.read()

# Replace draw_background
new_bg = """def draw_background(canvas, doc):
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
    canvas.restoreState()"""

text = re.sub(r'def draw_background\(canvas, doc\):.*?canvas\.restoreState\(\)', new_bg, text, flags=re.DOTALL)

# Replace the table style block in shortlist_bot.py
# First the title string
text = re.sub(r'colors\.HexColor\(\'#FFD700\'\)', "colors.HexColor('#FFD700')", text)

# TableStyle replacement
new_tablestyle = """t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#5D0000')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.HexColor('#FFD700')),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('GRID', (0,0), (-1,-1), 1.5, colors.HexColor('#FFD700')),
        ('BACKGROUND', (0,1), (-1,-1), colors.HexColor('#2A0808')),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.HexColor('#2A0808'), colors.HexColor('#08102A')]),
        ('TOPPADDING', (0,0), (-1,-1), 12), ('BOTTOMPADDING', (0,0), (-1,-1), 12),
        ('LEFTPADDING', (0,0), (-1,-1), 8), ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))"""

text = re.sub(r't\.setStyle\(TableStyle\(\[.*?\]\)\)', new_tablestyle, text, flags=re.DOTALL)

with open("shortlist_bot.py", "w") as f:
    f.write(text)

