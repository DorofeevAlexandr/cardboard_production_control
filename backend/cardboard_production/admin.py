from django.contrib import admin
from .models import Productions, Order, Material, Format

admin.site.site_header = "Панель администрирования"
admin.site.index_title = "Сменные задания"

@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    # Отображение полей в списке
    list_display = ('name', )
    # Фильтрация в списке
    # list_filter = ('name',)
    # Поиск по полям
    search_fields = ('name',)

@admin.register(Format)
class FormatAdmin(admin.ModelAdmin):
    # Отображение полей в списке
    list_display = ('format', )
    # Фильтрация в списке
    # list_filter = ('name',)
    # Поиск по полям
    search_fields = ('format',)

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

