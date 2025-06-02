from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
import uuid


class TimeStampedMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        # Этот параметр указывает Django, что этот класс не является представлением таблицы
        abstract = True


class UUIDMixin(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class Material(UUIDMixin, TimeStampedMixin):
    name = models.CharField(verbose_name='Материал', max_length=40, unique=True)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        db_table = 'material'
        verbose_name = 'Материал'
        verbose_name_plural = 'Материалы'


class Order(UUIDMixin, TimeStampedMixin):
    name = models.CharField(verbose_name='Имя заказа', max_length=40, unique=True)
    format = models.CharField(verbose_name='Формат', max_length=40)
    profile = models.CharField(verbose_name='Профиль', max_length=40)
    material_outer = models.ForeignKey('Material', verbose_name='Внешний материал', related_name='orders_material_outer', on_delete=models.CASCADE)
    material_corrugation = models.ForeignKey('Material', verbose_name='Материал гофрирования', related_name='orders_material_corrugation', on_delete=models.CASCADE)
    material_inside = models.ForeignKey('Material', verbose_name='Внутрений материал', related_name='orders_material_inside', on_delete=models.CASCADE)

    def __str__(self):
        return (f'{self.name} - {self.format} - {self.profile} ({self.material_outer} {self.material_corrugation} '
                f'{self.material_inside})')

    class Meta:
        db_table = 'order'
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'


class Productions(UUIDMixin, TimeStampedMixin):
    order_date = models.DateField(verbose_name='Дата')
    order = models.ForeignKey('Order', verbose_name='Заказ', on_delete=models.CASCADE)
    quantity = models.IntegerField(verbose_name='Количество',  validators=[MinValueValidator(0)])

    def __str__(self):
        return f'{self.order_date} - {self.order.__str__()} - {self.order} ({self.quantity})'

    class Meta:
        db_table = 'productions'
        verbose_name = 'Сменное задание'
        verbose_name_plural = 'Сменные задания'
