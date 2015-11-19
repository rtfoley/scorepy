from cStringIO import StringIO
from xhtml2pdf import pisa
from flask import make_response


# Create a PDF file from data
def create_pdf(pdf_data, filename):
    pdf = StringIO()
    pisa.CreatePDF(StringIO(pdf_data.encode('utf-8')), pdf, encoding="utf-8")
    response = make_response(pdf.getvalue())
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'inline; filename=%s.pdf' % \
                                              filename
    return response

