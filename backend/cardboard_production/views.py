import datetime as  dt
from django.shortcuts import render, redirect
from django.http import (HttpResponse, HttpResponseNotFound, Http404, HttpResponseRedirect,
                         HttpResponsePermanentRedirect, FileResponse)
import io
import mimetypes
import xlsxwriter

from .forms import ReadDateForElectroCounters, ReadMonthForElectroCounters
from .work_with_electrocouners import (get_counters_from_base, client_influxdb, read_electro_counters_values,
                                       get_reports_electro_counters, calculate_result_value, save_report_in_excel)
from .work_with_excel import statement_to_excel


menu = [{'title': "Показания счетчиков", 'url_name': 'electro_counters'},
        {'title': "Данные за день", 'url_name': 'electro_counters_statistics_for_the_day'},
        {'title': "Данные за месяц", 'url_name': 'electro_counters_statistics_for_the_month'},
        {'title': "Отчеты", 'url_name': 'reports'},
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


def electro_counters_value(request):
    counters = get_counters_from_base()
    title = f'Показания электросчетчиков'
    data = {
        'title': title,
        'counters': counters,
        'menu': menu,
    }
    return render(request, 'cardboard_production/electro_counters_value.html', context=data)


def electro_counters_statistics_for_the_day(request):
    count_values = []
    time = []
    counters = get_counters_from_base()
    title = f'Потребление электроэнергии - Данные за день'
    if request.method == 'POST':
        form = ReadDateForElectroCounters(request.POST, request.FILES)
        if form.is_valid():
            select_date = form.cleaned_data.get('day', None)
            if select_date:
                title = f'Потребление электроэнергии - Данные за {select_date.strftime('%d %B %Y')}г.'
                client = client_influxdb()
                time, count_values = read_electro_counters_values(client=client,
                                                                  date=select_date,
                                                                  data_reading_period='1 day',
                                                                  st_step_time='1h')
                client.close()
    else:
        form = ReadDateForElectroCounters()

    data = {
        'title': title,
        'counters': counters,
        'count_values': count_values,
        'form': form,
        'times': time,
        'menu': menu,
    }
    return render(request, 'cardboard_production/electro_counters.html', context=data)


def electro_counters_statistics_for_the_month(request):
    count_values = []
    time = []
    counters = get_counters_from_base()
    title = f'Потребление электроэнергии - Данные за месяц'
    if request.method == 'POST':
        form = ReadMonthForElectroCounters(request.POST, request.FILES)
        if form.is_valid():
            calendar_date = form.cleaned_data.get('start_day', None)
            title = f'Потребление электроэнергии - Данные за {calendar_date.strftime('%B %Y')}г.'
            start_date = dt.date(year=calendar_date.year,
                                 month=calendar_date.month,
                                 day=1)
            if start_date:
                client = client_influxdb()
                time, count_values = read_electro_counters_values(client=client,
                                                                  date=start_date,
                                                                  data_reading_period='1 month',
                                                                  st_step_time='1d')
                client.close()
    else:
        form = ReadMonthForElectroCounters()

    data = {
        'title': title,
        'counters': counters,
        'count_values': count_values,
        'form': form,
        'times': time,
        'menu': menu,
    }
    return render(request, 'cardboard_production/electro_counters.html', context=data)


def reports_for_the_month(request):
    reports = {}
    title = f'Потребление электроэнергии - Данные за месяц'
    if request.method == 'POST':
        form = ReadMonthForElectroCounters(request.POST, request.FILES)
        if form.is_valid():
            calendar_date = form.cleaned_data.get('start_day', None)
            title = f'Потребление электроэнергии - Данные за {calendar_date.strftime('%B %Y')}г.'
            start_date = dt.date(year=calendar_date.year,
                                 month=calendar_date.month,
                                 day=1)
            if start_date:
                client = client_influxdb()
                time, counter_values = read_electro_counters_values(client=client,
                                                                  date=start_date,
                                                                  data_reading_period='1 month',
                                                                  st_step_time='1h')
                reports = get_reports_electro_counters(counter_values, cur_month=start_date.month)
                calculate_result_value(reports)
                client.close()
                if 'b_save' in request.POST:
                    return save_report_in_excel(reports, start_date, title)
    else:
        form = ReadMonthForElectroCounters()


    data = {
        'title': title,
        'reports': reports,
        'form': form,
        'menu': menu,
    }
    return render(request, 'cardboard_production/electro_counters_report.html', context=data)


def download_statement(request, statement_date:str):

    output = io.BytesIO()
    workbook = xlsxwriter.Workbook(output)

    statement_to_excel(workbook, statement_date)

    workbook.close()
    output.seek(0)

    response = HttpResponse(output.read(),
                            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
                            )
    response['Content-Disposition'] = f'attachment; filename=Statement_{statement_date.replace('-','_')}.xlsx'
    return response
