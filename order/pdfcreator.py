# pdfcreator.py
from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa


def renderPdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)

    result = BytesIO()
    # UTF-8 ilə encode et (Azərbaycan hərfləri üçün daha yaxşı)
    pdf = pisa.pisaDocument(BytesIO(html.encode('UTF-8')), result)

    if not pdf.err:
        response = HttpResponse(result.getvalue(), content_type='application/pdf')
        # inline -> brauzerdə açılacaq; attachment -> birbaşa yüklənəcək
        response['Content-Disposition'] = 'inline; filename="order.pdf"'
        response['Content-Transfer-Encoding'] = 'binary'
        return response

    # PDF yaradılmayıbsa 500 qaytarmaq daha faydalıdır
    return HttpResponse('Xəta: PDF yaradılmadı', status=500)
