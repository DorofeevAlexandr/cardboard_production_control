from decimal import Decimal

import datetime as dt
from django.contrib import admin, messages
from django.utils.safestring import mark_safe
from .models import Productions, Order, Material, Format, Profile, CuttingCardboard, Statement

admin.site.site_header = "Панель администрирования"
admin.site.index_title = "Сменные задания"


@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    # Отображение полей в списке
    list_display = ('name', 'density', )
    # fields = [('name', 'density')]


@admin.register(Format)
class FormatAdmin(admin.ModelAdmin):
    # Отображение полей в списке
    list_display = ('format', )
    # list_display_links = None


@admin.register(Profile)
class FormatAdmin(admin.ModelAdmin):
    # Отображение полей в списке
    list_display = ('name', )


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    # Отображение полей в списке
    fields = ('name', 'profile', 'color_count', 'stamp', 'width', 'length', 'area', 'set_area',
              ('scheme_file', 'file',), ('scheme_file_2', 'file2',),
              ('view_design_file', 'design_file',), ('view_equipment_file', 'equipment_file',),
              'material_outer', 'material_corrugation', 'material_inside')
    list_display = ('name', 'profile', 'color_count', 'stamp', 'width', 'length', 'area', 'set_area',
                    'scheme_file', 'scheme_file_2', 'view_design_file', 'view_equipment_file',
                    'material_outer', 'material_corrugation', 'material_inside')
    readonly_fields = ['area', 'scheme_file', 'scheme_file_2', 'view_design_file', 'view_equipment_file']
    # Фильтрация в списке
    # list_filter = ('name', 'format',)
    # Поиск по полям
    search_fields = ('name', )
    # save_on_top = True

    @admin.display(description="Чертёж 1", ordering='name')
    def scheme_file(self, order: Order):
        if order.file:
            return mark_safe(f"<a href='{order.file.url}'target='_blank'><img src='{order.file.url}' width=50></a>")
        return "Без чертежа"

    @admin.display(description="Чертёж 2", ordering='name')
    def scheme_file_2(self, order: Order):
        if order.file2:
            return mark_safe(f"<a href='{order.file2.url}'target='_blank'><img src='{order.file2.url}' width=50></a>")
        return "Без чертежа"

    @admin.display(description="Дизайн", ordering='name')
    def view_design_file(self, order: Order):
        if order.design_file:
            return mark_safe(f"<a href='{order.design_file.url}'target='_blank'><img src='{order.design_file.url}' width=50></a>")
        return "Без дизайна"

    @admin.display(description="Комплектация", ordering='name')
    def view_equipment_file(self, order: Order):
        if order.equipment_file:
            return mark_safe(f"<a href='{order.equipment_file.url}'target='_blank'><img src='{order.equipment_file.url}' width=50></a>")
        return "Без комплектации"


@admin.register(Productions)
class ProductionsAdmin(admin.ModelAdmin):
    # Отображение полей в списке
    list_display = ('order_date', 'order', 'quantity', 'order_status')
    # Фильтрация в списке
    # list_filter = ('order_date', 'order')
    # Поиск по полям
    # search_fields = ('order_date', 'order')
    list_editable = ('order_status',)
    date_hierarchy = "order_date"
    actions = ['set_status_queue', 'set_status_in_production', 'set_status_manufactured']

    @admin.action(description="Поставить в очередь выбранные заказы")
    def set_status_queue(self, request, queryset):
        count = queryset.update(order_status=Productions.Status.IN_THE_QUEUE)
        self.message_user(request, f"{count} заказов поставлено в очередь!", messages.WARNING)

    @admin.action(description="Поставить в производство выбранные заказы")
    def set_status_in_production(self, request, queryset):
        count = queryset.update(order_status=Productions.Status.IS_IN_PRODUCTION)
        self.message_user(request, f"{count} заказов оправлено в производство!", messages.WARNING)

    @admin.action(description="Отметить изготовлеными выбранные заказы")
    def set_status_manufactured(self, request, queryset):
        count = queryset.update(order_status=Productions.Status.MANUFACTURED)
        self.message_user(request, f"{count} заказов изготовлено!", messages.WARNING)


def cutting_info_add_rows(prod: Productions):
    if prod:
        return (f"<tr>"
                f"<td>{prod.order_date}</td>"
                f"<td>{prod.order.name}</td>"
                f"<td>{prod.order.profile}</td>"
                f"<td>{prod.order.width}</td>"
            f"</tr>" )
    else:
        return ''

@admin.register(CuttingCardboard)
class CuttingCardboardAdmin(admin.ModelAdmin):
    # Отображение полей в списке
    list_display = ('format', 'cutting_info', 'trim_info')
    date_hierarchy = "order1__order_date"

    @admin.display(description="Выбранные заказы")
    def cutting_info(self, cutting: CuttingCardboard):
        html_text =  (f"<table>"
            f"<tr>"
                f"<td>Дата</td>"
                f"<td>Заказ</td>"
                f"<td>Профиль</td>"
                f"<td>Ширина</td>"
            f"</tr>")
        html_text += cutting_info_add_rows(cutting.order1)
        html_text += cutting_info_add_rows(cutting.order2)
        html_text += cutting_info_add_rows(cutting.order3)
        html_text += cutting_info_add_rows(cutting.order4)
        html_text += cutting_info_add_rows(cutting.order5)
        html_text += cutting_info_add_rows(cutting.order6)
        html_text += f"</table>"
        return mark_safe(html_text)

    @admin.display(description="Обрезь / Обрезь в %")
    def trim_info(self, cutting: CuttingCardboard):
        cutting_format = float(cutting.format.format) if cutting.format else 0
        width_order_1 = int(cutting.order1.order.width) if cutting.order1 else 0
        width_order_2 = int(cutting.order2.order.width) if cutting.order2 else 0
        width_order_3 = int(cutting.order3.order.width) if cutting.order3 else 0
        width_order_4 = int(cutting.order4.order.width) if cutting.order4 else 0
        width_order_5 = int(cutting.order5.order.width) if cutting.order5 else 0
        width_order_6 = int(cutting.order6.order.width) if cutting.order6 else 0

        width_order = (width_order_1 + width_order_2 + width_order_3 +
                       width_order_4 + width_order_5 + width_order_6)
        trim = int(cutting_format - width_order)
        if format != 0:
            trim_percent = int(float(trim) / float(cutting_format) * 100)
        else:
            trim_percent = 0
        return f"{trim} / {trim_percent}%"


@admin.register(Statement)
class StatementAdmin(admin.ModelAdmin):
    # Отображение полей в списке
    fields = ('statement_date', 'order', 'statement_start_time',
              'statement_end_time', 'downtime', 'quantity_sent_production', 'quantity_manufactured')
    list_display = ('statement_date', 'order',
                    'color_count', 'stamp', 'width', 'length', 'area',
                    'statement_start_time', 'statement_end_time', 'minutes', 'downtime',
                    'quantity_sent_production', 'quantity_manufactured',
                    'defects_percent', 'speed_manufactured', )
    # readonly_fields = ['order__stamp', 'order__width', 'order__length', 'order__area',]
    # Фильтрация в списке
    # list_filter = ('name', 'format',)
    # Поиск по полям
    # search_fields = ('name', )
    # save_on_top = True

    @admin.display(description="Печать")
    def color_count(self, statement: Statement):
        if statement.order:
            return statement.order.color_count
        return "-"

    @admin.display(description="Штамп")
    def stamp(self, statement: Statement):
        if statement.order:
            return statement.order.stamp
        return "-"

    @admin.display(description="Ширина, мм")
    def width(self, statement: Statement):
        if statement.order:
            return statement.order.width
        return "-"

    @admin.display(description="Длина, мм")
    def length(self, statement: Statement):
        if statement.order:
            return statement.order.length
        return "-"

    @admin.display(description="Площадь, м²")
    def area(self, statement: Statement):
        if statement.order:
            return statement.order.area
        return "-"

    def get_minutes(self, statement: Statement):
        try:
            if statement.statement_end_time and statement.statement_start_time:
                start_time = dt.datetime.combine(statement.statement_date, statement.statement_start_time)
                end_time = dt.datetime.combine(statement.statement_date, statement.statement_end_time)
                return int((end_time - start_time).total_seconds() // 60)
            else:
                return  "-"
        except:
            return "-"

    @admin.display(description="Минуты")
    def minutes(self, statement: Statement):
        return self.get_minutes(statement)

    @admin.display(description="Брак, %")
    def defects_percent(self, statement: Statement):
        try:
            if statement.quantity_sent_production and statement.quantity_manufactured:
                k_defects = (statement.quantity_sent_production - statement.quantity_manufactured) / statement.quantity_manufactured
                result = round(k_defects * 100.0, 1)
                return result
            else:
                return  "-"
        except:
            return "-"

    @admin.display(description="Произведено, шт/мин")
    def speed_manufactured(self, statement: Statement):
        try:
            if statement.quantity_manufactured:
                return round(statement.quantity_manufactured / self.get_minutes(statement))
            else:
                return  "-"
        except:
            return "-"
