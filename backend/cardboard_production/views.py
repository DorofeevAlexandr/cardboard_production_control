from django.shortcuts import render, redirect
from django.http import (HttpResponse, HttpResponseNotFound, Http404, HttpResponseRedirect,
                         HttpResponsePermanentRedirect, FileResponse)
import mimetypes

from .forms import ReadDataCounters, ReadAndSaveLinesStatistic
from .work_with_electrocouners import get_counters_from_base, client_influxdb, read_electro_counters_values


menu = [{'title': "Данные за день", 'url_name': 'electro_counters_statistics_for_the_day'},
        {'title': "Данные за месяц", 'url_name': 'electro_counters_statistics_for_the_month'},
        {'title': "Настройка", 'url_name': 'tuning'},
]

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


def electro_counters_statistics_for_the_day(request):
    count_values = []
    time = []
    counters = get_counters_from_base()
    if request.method == 'POST':
        form = ReadDataCounters(request.POST, request.FILES)
        if form.is_valid():
            select_date = form.cleaned_data.get('day', None)
            if select_date:
                pass
                client = client_influxdb()
                time, count_values = read_electro_counters_values(client=client,
                                             date=select_date)
                client.close()
    else:
        form = ReadDataCounters()

    data = {
        'title': 'Электросчетчики - Данные за день',
        'counters': counters,
        'count_values': count_values,
        'form': form,
        'times': time,
        'menu': menu,
    }
    return render(request, 'cardboard_production/electro_counters_in_day.html', context=data)
