from django.contrib import admin
from .models import Productions, Order, Material, Format, Profile, CuttingCardboard

admin.site.site_header = "Панель администрирования"
admin.site.index_title = "Сменные задания"


@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    # Отображение полей в списке
    list_display = ('name', 'density', )


@admin.register(Format)
class FormatAdmin(admin.ModelAdmin):
    # Отображение полей в списке
    list_display = ('format', )


@admin.register(Profile)
class FormatAdmin(admin.ModelAdmin):
    # Отображение полей в списке
    list_display = ('name', )


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    # Отображение полей в списке
    list_display = ('name', 'profile', 'material_outer', 'material_corrugation', 'material_inside')
    # Фильтрация в списке
    # list_filter = ('name', 'format',)
    # Поиск по полям
    search_fields = ('name', 'format',)


@admin.register(Productions)
class ProductionsAdmin(admin.ModelAdmin):
    # Отображение полей в списке
    list_display = ('order_date', 'order', 'quantity', 'order_status')
    # Фильтрация в списке
    # list_filter = ('order_date', 'order')
    # Поиск по полям
    search_fields = ('order_date', 'order')


@admin.register(CuttingCardboard)
class CuttingCardboardAdmin(admin.ModelAdmin):
    # Отображение полей в списке
    list_display = ('format', 'cutting_info')

    @admin.display(description="Краткое описание")
    def cutting_info(self, cutting: CuttingCardboard):

        return (f'{cutting.order1} \n {cutting.order2} \n {cutting.order3} \n '
                f'{cutting.order4} \n {cutting.order5} \n {cutting.order6} \n')
