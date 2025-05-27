from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound, Http404, HttpResponseRedirect, HttpResponsePermanentRedirect


def page_not_found(request, exception):
    return HttpResponseNotFound("<h1>Страница не найдена</h1>")
