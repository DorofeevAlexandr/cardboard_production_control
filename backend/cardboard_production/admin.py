from django.contrib import admin
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
    date_hierarchy = "order_date"


@admin.register(CuttingCardboard)
class CuttingCardboardAdmin(admin.ModelAdmin):
    # Отображение полей в списке
    list_display = ('format', 'cutting_info')
    date_hierarchy = "order1__order_date"

    @admin.display(description="Краткое описание")
    def cutting_info(self, cutting: CuttingCardboard):

        return (f'{cutting.order1} \n {cutting.order2} \n {cutting.order3} \n '
                f'{cutting.order4} \n {cutting.order5} \n {cutting.order6} \n')
