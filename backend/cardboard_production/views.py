from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseNotFound, Http404, HttpResponseRedirect, HttpResponsePermanentRedirect

from pdf_view.views.pdf_view import PDFView


def tuning(request):
    return HttpResponse("<h1>Tuning</h1>")

def index(request):
    return redirect('/admin')

def page_not_found(request, exception):
    return HttpResponseNotFound("<h1>Страница не найдена</h1>")


class MyPDFView(PDFView):
    template_name = 'my_app/my_pdf.html'
    title = 'My PDF Document' # optional
    filename = 'My PDF.pdf' # optional
    css_paths = [ # optional
        'my_pdf/css/my_pdf.css',
    ]