from django.contrib import admin
from .models import Productions, Order, Material, Format, Density, Profile

admin.site.site_header = "Панель администрирования"
admin.site.index_title = "Сменные задания"

@admin.register(Density)
class FormatAdmin(admin.ModelAdmin):
    # Отображение полей в списке
    list_display = ('density', )

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
    list_display = ('name', 'format', 'profile', 'material_outer', 'material_corrugation', 'material_inside')
    # Фильтрация в списке
    # list_filter = ('name', 'format',)
    # Поиск по полям
    search_fields = ('name', 'format',)

@admin.register(Productions)
class ProductionsAdmin(admin.ModelAdmin):
    # Отображение полей в списке
    list_display = ('order_date', 'order', 'quantity',)
    # Фильтрация в списке
    # list_filter = ('order_date', 'order')
    # Поиск по полям
    search_fields = ('order_date', 'order')

