from django.contrib import admin, messages
from django.utils.safestring import mark_safe
from .models import Productions, Order, Material, Format, Profile, CuttingCardboard

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
    fields = ('name', 'profile', 'width', 'length', 'file', 'scheme_file', 'material_outer', 'material_corrugation',
                    'material_inside')
    list_display = ('name', 'profile', 'width', 'length', 'scheme_file', 'material_outer', 'material_corrugation', 'material_inside')
    readonly_fields = ['scheme_file']
    # Фильтрация в списке
    # list_filter = ('name', 'format',)
    # Поиск по полям
    search_fields = ('name', 'format',)
    save_on_top = True

    @admin.display(description="Изображение схемы", ordering='name')
    def scheme_file(self, order: Order):
        if order.file:
            return mark_safe(f"<a href='{order.file.url}'target='_blank'><img src='{order.file.url}' width=50></a>")
        return "Без схемы"


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
    list_display = ('format', 'cutting_info')
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
        width_order = (int(cutting.order1.order.width) +
                int(cutting.order2.order.width) +
                int(cutting.order3.order.width) +
                int(cutting.order4.order.width) +
                int(cutting.order5.order.width) +
                int(cutting.order6.order.width))
        trim = int(cutting.format.format) - width_order
        # if cutting.format and (cutting.format != 0):
        #     trim_percent = float(trim) / float(cutting.format) * 100
        # else:
        #     trim_percent = 0
        return f"{width_order} {trim}"
