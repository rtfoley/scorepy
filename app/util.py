from cStringIO import StringIO
from xhtml2pdf import pisa


# Create a PDF file from data
def create_pdf(pdf_data):
    pdf = StringIO()
    pisa.CreatePDF(StringIO(pdf_data.encode('utf-8')), pdf, encoding="utf-8")
    return pdf
