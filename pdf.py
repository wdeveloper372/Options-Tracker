from reportlab.pdfgen import canvas
from reportlab.lib import colors
# from options import or

def create_pdf(filename, data):
    c = canvas.Canvas(filename)
    c.setFillColor(colors.black)
    for i, row in enumerate(data):
        c.drawString(100, 750 - i * 20, f"{row[0]} - {row[1]}")
    c.save()

create_pdf("options.pdf", order.sample_data)