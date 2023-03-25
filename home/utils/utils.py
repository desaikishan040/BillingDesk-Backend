from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from django.template import Context

import pdfkit


async def render_to_pdf(template_src, context_dict):
    template = get_template(template_src)
    html = template.render(context_dict)
    pdf = await pdfkit.from_file(html, "ourcodeworld.pdf")
    #
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="ourcodeworld.pdf"'

    return pdf