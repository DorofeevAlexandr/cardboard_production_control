import datetime as dt
from pprint import pprint

import xlsxwriter

from .models import Statement


def get_minutes(product: Statement):
    try:
        if product.statement_end_time and product.statement_start_time:
            start_time = dt.datetime.combine(product.statement_date, product.statement_start_time)
            end_time = dt.datetime.combine(product.statement_date, product.statement_end_time)
            return int((end_time - start_time).total_seconds() // 60)
        else:
            return "-"
    except:
        return "-"


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
        return "-"
    except:
        return "-"


def statement_to_excel(workbook:xlsxwriter.Workbook, statement_date:str):
    worksheet = workbook.add_worksheet('Ведомость')

    worksheet.set_column(0, 0, 10)
    worksheet.set_column(1, 1, 40)
    worksheet.set_column(2, 3, 10)
    worksheet.set_column(4, 6, 12)
    worksheet.set_column(7, 9, 10)
    worksheet.set_column(10, 16, 12)

    bold_format = workbook.add_format({'bold': True, 'border': 2, 'align': 'center'})
    left_format = workbook.add_format({'bold': False, 'border': 1})
    def_format = workbook.add_format({'bold': False, 'border': 1, 'align': 'center'})

    worksheet.write(6, 6, 'Ведомость  данных изготовления  продукции на линиях')

    row_offset = 8
    worksheet.write(row_offset, 0, 'дата', bold_format)
    worksheet.write(row_offset, 1, 'продукция', bold_format)
    worksheet.write(row_offset, 2, 'печать', bold_format)
    worksheet.write(row_offset, 3, 'штамп', bold_format)
    worksheet.write(row_offset, 4, 'ширина,мм', bold_format)
    worksheet.write(row_offset, 5, 'длина мм', bold_format)
    worksheet.write(row_offset, 6, 'площадь', bold_format)
    worksheet.write(row_offset, 7, 'начало', bold_format)
    worksheet.write(row_offset, 8, 'окончан', bold_format)
    worksheet.write(row_offset, 9, 'минуты', bold_format)
    worksheet.write(row_offset, 10, 'пропущено', bold_format)
    worksheet.write(row_offset, 11, 'изготовлено', bold_format)
    worksheet.write(row_offset, 12, '% брака', bold_format)
    worksheet.write(row_offset, 13, 'произ.шт/мин', bold_format)
    worksheet.write(row_offset, 14, 'простой', bold_format)
    worksheet.write(row_offset, 15, 'общие м2', bold_format)

    queryset = Statement.objects.filter(statement_date=statement_date).order_by('statement_start_time')
    print(queryset)
    for product in queryset:
        row_offset += 1
        worksheet.write(row_offset, 0, product.statement_date.strftime('%d.%m.%Y'), def_format)
        worksheet.write(row_offset, 1, product.order.name, left_format)
        color_count = str(product.order.color_count) if product.order.color_count != 0 else '-'
        worksheet.write(row_offset, 2, color_count, def_format)
        stamp = '+' if product.order.stamp else '-'
        worksheet.write(row_offset, 3, stamp, def_format)
        worksheet.write(row_offset, 4, product.order.width, def_format)
        worksheet.write(row_offset, 5, product.order.length, def_format)
        worksheet.write(row_offset, 6, product.order.area, def_format)
        worksheet.write(row_offset, 7, product.statement_start_time.strftime('%H:%M'), def_format)
        worksheet.write(row_offset, 8, product.statement_end_time.strftime('%H:%M'), def_format)
        worksheet.write(row_offset, 9, get_minutes(product), def_format)
        worksheet.write(row_offset, 10, product.quantity_sent_production, def_format)
        worksheet.write(row_offset, 11, product.quantity_manufactured, def_format)
        worksheet.write(row_offset, 12, defects_percent(product), def_format)
        worksheet.write(row_offset, 13, speed_manufactured(product), def_format)
        worksheet.write(row_offset, 14, '', def_format)
        worksheet.write(row_offset, 15, manufactured_area(product), def_format)

        pprint(product.statement_date.strftime('%d.%m.%Y'))
        pprint(product.order.name)

