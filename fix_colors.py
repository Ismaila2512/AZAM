with open("shortlist_bot.py", "r") as f:
    text = f.read()

import re

new_draw_bg = """def draw_background(canvas, doc):
    from reportlab.lib import colors
    canvas.saveState()
    canvas.setFillColor(colors.HexColor('#050101'))
    canvas.rect(0, 0, doc.pagesize[0], doc.pagesize[1], fill=1)
    canvas.setFillColor(colors.HexColor('#3a0000'))
    canvas.circle(0, doc.pagesize[1], 250, fill=1, stroke=0)
    canvas.setStrokeColor(colors.HexColor('#FFD700'))
    canvas.setLineWidth(3)
    canvas.line(doc.pagesize[0] - 50, doc.pagesize[1], doc.pagesize[0] - 100, doc.pagesize[1] - 80)
    canvas.line(doc.pagesize[0] - 100, doc.pagesize[1] - 80, doc.pagesize[0] - 40, doc.pagesize[1] - 80)
    canvas.line(doc.pagesize[0] - 40, doc.pagesize[1] - 80, doc.pagesize[0] - 120, doc.pagesize[1] - 200)
    canvas.restoreState()"""

text = re.sub(r'def draw_background\(canvas, doc\):.*?canvas\.restoreState\(\)', new_draw_bg, text, flags=re.DOTALL)

text = text.replace("'#10b981'", "'#FFD700'")
text = text.replace("'#34d399'", "'#ff6666'")
text = text.replace("'#064e3b'", "'#5D0000'")
text = text.replace("'#059669'", "'#B00000'")
text = text.replace("'#022c22'", "'#1a0000'")

with open("shortlist_bot.py", "w") as f:
    f.write(text)
