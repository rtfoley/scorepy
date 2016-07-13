from cStringIO import StringIO
from xhtml2pdf import pisa
from flask import make_response
from app.teams.models import Team


# Create a PDF file from data
def create_pdf(pdf_data, filename):
    pdf = StringIO()
    pisa.CreatePDF(StringIO(pdf_data.encode('utf-8')), pdf, encoding="utf-8")
    response = make_response(pdf.getvalue())
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'inline; filename=%s.pdf' % \
                                              filename
    return response

def sortTeamsWithPlaceholder(teams):
    placeholder = Team(number='Select',
                       name='Select',
                       affiliation='Select',
                       city='Select',
                       state='Select',
                       is_rookie=False)
    placeholder.id = -1
    sortedTeams = sorted(teams, key=by_team)
    sortedTeams.insert(0, placeholder)

    return sortedTeams

# Sort teams by number
def by_team(team):
    return team.number
