from django.shortcuts import render, redirect
from django.http import (HttpResponse, HttpResponseNotFound, Http404, HttpResponseRedirect,
                         HttpResponsePermanentRedirect, FileResponse)

import mimetypes


def tuning(request):
    return HttpResponse("<h1>Tuning</h1>")

def index(request):
    return redirect('/admin')

def page_not_found(request, exception):
    return HttpResponseNotFound("<h1>Страница не найдена</h1>")

def open_pdf_file_view(request, filename):
    mimetype = mimetypes.guess_type(filename)
    app_type = mimetype[0]
    app_type = 'application/pdf'
    data = {
        'title': filename,
        'app_type': app_type,
        'filename': f'/{filename}',
    }
    return render(request, 'cardboard_production/open_pdf.html', context=data)
