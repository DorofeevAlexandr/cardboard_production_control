import datetime as dt
from pprint import pprint

import xlsxwriter

from .models import Statement


def get_working_minutes(product: Statement):
    try:
        if product.statement_end_time and product.statement_start_time:
            start_time = dt.datetime.combine(product.statement_date, product.statement_start_time)
            end_time = dt.datetime.combine(product.statement_date, product.statement_end_time)
            return int((end_time - start_time).total_seconds() // 60)
        else:
            return 0
    except:
        return 0


def defects_percent(product: Statement):
    try:
        if product.quantity_sent_production and product.quantity_manufactured:
            k_defects = (product.quantity_sent_production - product.quantity_manufactured) / product.quantity_manufactured
            result = round(k_defects * 100.0, 1)
            return result
        else:
            return  "-"
    except:
        return "-"


def speed_manufactured(product: Statement):
    try:
        if product.quantity_manufactured:
            return round(product.quantity_manufactured / get_minutes(product))
        else:
            return  "-"
    except:
        return "-"


def manufactured_area(product: Statement):
    try:
        if product.order and product.quantity_manufactured:
            area = product.order.width * product.order.length * product.quantity_manufactured / (1000 * 1000)
            return round(area)
        return 0
    except:
        return 0


def statement_to_excel(workbook:xlsxwriter.Workbook, statement_date:str):
    ws = workbook.add_worksheet('Ведомость')

    ws.set_column(0, 0, 10)
    ws.set_column(1, 1, 40)
    ws.set_column(2, 3, 10)
    ws.set_column(4, 6, 12)
    ws.set_column(7, 9, 10)
    ws.set_column(10, 16, 12)

    bold_format = workbook.add_format({'bold': True, 'border': 2, 'align': 'center'})
    left_format = workbook.add_format({'bold': False, 'border': 1})
    def_format = workbook.add_format({'bold': False, 'border': 1, 'align': 'center'})

    ws.write(2, 6, 'Ведомость  данных изготовления  продукции на линиях')

    row_offset = 4
    ws.write(row_offset, 0, 'дата', bold_format)
    ws.write(row_offset, 1, 'продукция', bold_format)
    ws.write(row_offset, 2, 'печать', bold_format)
    ws.write(row_offset, 3, 'штамп', bold_format)
    ws.write(row_offset, 4, 'ширина,мм', bold_format)
    ws.write(row_offset, 5, 'длина мм', bold_format)
    ws.write(row_offset, 6, 'площадь', bold_format)
    ws.write(row_offset, 7, 'начало', bold_format)
    ws.write(row_offset, 8, 'окончан', bold_format)
    ws.write(row_offset, 9, 'минуты', bold_format)
    ws.write(row_offset, 10, 'пропущено', bold_format)
    ws.write(row_offset, 11, 'изготовлено', bold_format)
    ws.write(row_offset, 12, '% брака', bold_format)
    ws.write(row_offset, 13, 'произ.шт/мин', bold_format)
    ws.write(row_offset, 14, 'простой', bold_format)
    ws.write(row_offset, 15, 'общие м2', bold_format)

    summ_working_minutes = 0
    summ_quantity_manufactured = 0
    summ_manufactured_area = 0

    queryset = Statement.objects.filter(statement_date=statement_date).order_by('statement_start_time')
    print(queryset)
    for product in queryset:
        row_offset += 1
        ws.write(row_offset, 0, product.statement_date.strftime('%d.%m.%Y'), def_format)
        ws.write(row_offset, 1, product.order.name, left_format)
        color_count = str(product.order.color_count) if product.order.color_count != 0 else '-'
        ws.write(row_offset, 2, color_count, def_format)
        stamp = '+' if product.order.stamp else '-'
        ws.write(row_offset, 3, stamp, def_format)
        ws.write(row_offset, 4, product.order.width, def_format)
        ws.write(row_offset, 5, product.order.length, def_format)
        ws.write(row_offset, 6, product.order.area, def_format)
        ws.write(row_offset, 7, product.statement_start_time.strftime('%H:%M'), def_format)
        ws.write(row_offset, 8, product.statement_end_time.strftime('%H:%M'), def_format)
        summ_working_minutes += get_working_minutes(product)
        ws.write(row_offset, 9, get_working_minutes(product), def_format)
        ws.write(row_offset, 10, product.quantity_sent_production, def_format)
        summ_quantity_manufactured += product.quantity_manufactured
        ws.write(row_offset, 11, product.quantity_manufactured, def_format)
        ws.write(row_offset, 12, defects_percent(product), def_format)
        ws.write(row_offset, 13, speed_manufactured(product), def_format)
        ws.write(row_offset, 14, '', def_format)
        summ_manufactured_area += manufactured_area(product)
        ws.write(row_offset, 15, manufactured_area(product), def_format)

    row_offset += 1
    ws.write(row_offset, 0, 'Итого', bold_format)
    ws.write(row_offset, 1, '', bold_format)
    ws.write(row_offset, 2, '', bold_format)
    ws.write(row_offset, 3, '', bold_format)
    ws.write(row_offset, 4, '', bold_format)
    ws.write(row_offset, 5, '', bold_format)
    ws.write(row_offset, 6, '', bold_format)
    ws.write(row_offset, 7, '', bold_format)
    ws.write(row_offset, 8, '', bold_format)
    ws.write(row_offset, 9, summ_working_minutes, bold_format)
    ws.write(row_offset, 10, '', bold_format)
    ws.write(row_offset, 11, summ_quantity_manufactured, bold_format)
    ws.write(row_offset, 12, '', bold_format)
    ws.write(row_offset, 13, '', bold_format)
    ws.write(row_offset, 14, '', bold_format)
    ws.write(row_offset, 15, summ_manufactured_area, bold_format)

    ws.print_area(0, 0, 15, 15)
    ws.set_paper(9)
    ws.set_landscape()
    ws.fit_to_pages(1, 1)
