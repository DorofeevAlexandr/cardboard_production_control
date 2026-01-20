from django.shortcuts import render, redirect
from django.http import (HttpResponse, HttpResponseNotFound, Http404, HttpResponseRedirect,
                         HttpResponsePermanentRedirect, FileResponse)


def tuning(request):
    return HttpResponse("<h1>Tuning</h1>")

def index(request):
    return redirect('/admin')

def page_not_found(request, exception):
    return HttpResponseNotFound("<h1>Страница не найдена</h1>")

def open_pdf_file_view(request, filename):
    try:
        return FileResponse(open(filename, 'rb'))
        # , content_type = 'application/pdf'
    except FileNotFoundError:
        raise Http404()
