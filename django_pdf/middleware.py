#!/usr/bin/env python
# TODO : pdf generation consume heavy ressources -> store pdf in media path and
#       test about age|modification before render or give from cache
import os.path
from xhtml2pdf import pisa
import cStringIO as StringIO
from django.http import HttpResponse
from django.conf import settings
import urllib
import re

REQUEST_FORMAT_NAME = getattr(settings, 'REQUEST_FORMAT_NAME', 'format')
REQUEST_FORMAT_PDF_VALUE = getattr(settings, 'REQUEST_FORMAT_PDF_VALUE', 'pdf')
TEMPLATE_PDF_CHECK = getattr(settings, 'TEMPLATE_PDF_CHECK','DJANGO_PDF_OUTPUT')
PDF_BASE_NAME =  getattr(settings, 'PDF_BASE_NAME','Mysite')


def fetch_resources(uri, rel):
    """
    Prepares paths for pisa
    Remember : you fetch for 'printing' so create a 'media=print' css import in your template
    # TODO test on server ( without ./manage.py runserver )
    """
    if re.match(".*%s.*"%settings.MEDIA_URL,uri):
	path = os.path.join(settings.MEDIA_ROOT,uri.replace(settings.MEDIA_URL, ""))

    if re.match(".*%s.*"%settings.STATIC_URL,uri):
	path = os.path.join(settings.STATIC_ROOT,uri.replace(settings.STATIC_URL, ""))
    return path


def transform_to_pdf(response,pdfname):
    """
    call xhtml2pdf.pisa to convert html responce to pdf
    """
    #response['mimetype'] = 'application/pdf'

    # TODO : on the fly filename from url
    #response['Content-Disposition'] = 'attachment; filename=%s.pdf' % pdfname

    content = response.content
    new_response = HttpResponse(content="",mimetype='application/pdf')
    new_response['Content-Disposition'] = 'attachment; filename=%s.pdf' % pdfname
    
    pdf = pisa.pisaDocument(StringIO.StringIO(content),
                            new_response, link_callback=fetch_resources)

    if not pdf.err:
        return new_response
    else:
        # TODO return error and redirect to default view
        return HttpResponse('We had some errors in pdfMiddleWare : \
                            <br/><pre>%s</pre>'%pdf)

class PdfMiddleware(object):
    """
    Converts the response to a pdf one if requested by '?format=pdf'
    """
    def process_response(self, request, response):
        reqformat = request.GET.get(REQUEST_FORMAT_NAME, None)
        req_pdfname = request.GET.get("pdfname",None)
        if reqformat == REQUEST_FORMAT_PDF_VALUE:
            if req_pdfname:
                pdfname = urllib.unquote(req_pdfname).replace('/','-')
            else:
                pdfname = '%s%s'%(PDF_BASE_NAME, request.path.replace('/','_'))
            response = transform_to_pdf(response,pdfname)
        return response
