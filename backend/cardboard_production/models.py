from decimal import Decimal

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
import uuid

from .custom_validator import custom_file_validator


class TimeStampedMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        # Этот параметр указывает Django, что этот класс не является представлением таблицы
        abstract = True


class UUIDMixin(models.Model):
    # id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    id = models.AutoField(primary_key=True, editable=False)

    class Meta:
        abstract = True


class Material(UUIDMixin, TimeStampedMixin):
    name = models.CharField(verbose_name='Материал', max_length=40)
    density = models.IntegerField(verbose_name='Плотность, г/м²', default=100, validators=[MinValueValidator(0)])

    def __str__(self):
        return f'{self.name}-{self.density}'

    class Meta:
        db_table = 'material'
        verbose_name = 'Материал слоя'
        verbose_name_plural = 'Материалы слоев'
        unique_together = ('name', 'density')


class Profile(UUIDMixin, TimeStampedMixin):
    name = models.CharField(verbose_name='Профиль', max_length=2)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        db_table = 'profile'
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'


class Format(UUIDMixin, TimeStampedMixin):
    format = models.IntegerField(verbose_name='Формат, мм',  validators=[MinValueValidator(0), MaxValueValidator(3000)])

    def __str__(self):
        return f'{self.format}'

    class Meta:
        db_table = 'format'
        verbose_name = 'Формат'
        verbose_name_plural = 'Форматы'


class Order(UUIDMixin, TimeStampedMixin):
    name = models.CharField(verbose_name='Наименование изделия', max_length=40, unique=True)
    profile = models.ForeignKey('Profile', verbose_name='Профиль', related_name='orders_profile', on_delete=models.CASCADE)
    width = models.IntegerField(verbose_name='Ширина, мм', default=100,  validators=[MinValueValidator(0), MaxValueValidator(3000)])
    length = models.IntegerField(verbose_name='Длина, мм', default=100,  validators=[MinValueValidator(0), MaxValueValidator(3000)])
    area = models.FloatField(verbose_name="Площадь м²", default=0)
    file = models.FileField(upload_to="Scheme/%Y/%m/", default=None,
                              blank=True, null=True, verbose_name="Cхема", validators=[custom_file_validator])
    material_outer = models.ForeignKey('Material', verbose_name='Наружный слой', related_name='orders_material_outer', on_delete=models.CASCADE)
    material_corrugation = models.ForeignKey('Material', verbose_name='Гофрирующий слой', related_name='orders_material_corrugation', on_delete=models.CASCADE)
    material_inside = models.ForeignKey('Material', verbose_name='Внутрений слой', related_name='orders_material_inside', on_delete=models.CASCADE)

    def calculate_area(self):
        if self.width and self.length:
            square = self.width * self.length
            square = Decimal(square) / (1000 * 1000)
            square = round(square, 3)
        else:
            square = 0
        return square

    def save(self, *args, **kwargs):
        self.area = self.calculate_area()
        super(Order, self).save(*args, **kwargs)

    def __str__(self):
        return (f'{self.name} - {self.profile} ({self.material_outer} | {self.material_corrugation} | '
                f'{self.material_inside})')

    class Meta:
        db_table = 'order'
        verbose_name = 'Изделие'
        verbose_name_plural = 'Изделия'


class Productions(UUIDMixin, TimeStampedMixin):
    class Status(models.IntegerChoices):
        IN_THE_QUEUE  = 0, 'В очереди'
        IS_IN_PRODUCTION = 1, 'В производстве'
        MANUFACTURED = 2, 'Изготовленно'
    order_date = models.DateField(verbose_name='Дата')
    order = models.ForeignKey('Order', verbose_name='Заказ', on_delete=models.CASCADE)
    quantity = models.IntegerField(verbose_name='Количество',  validators=[MinValueValidator(0)])
    order_status = models.IntegerField(choices=Status.choices,
                                       default=Status.IN_THE_QUEUE, verbose_name="Статус заказа")

    def __str__(self):
        return f'{self.order_date} - {self.order} ({self.quantity})'

    class Meta:
        db_table = 'productions'
        verbose_name = 'Сменное задание'
        verbose_name_plural = 'Сменные задания'


class CuttingCardboard(UUIDMixin, TimeStampedMixin):
    format = models.ForeignKey('Format', verbose_name='Формат, мм', related_name='orders_format', on_delete=models.CASCADE)
    order1 = models.ForeignKey('Productions', verbose_name='Заказ 1', on_delete=models.CASCADE, related_name='cutting_order_1', blank=True, null=True)
    order2 = models.ForeignKey('Productions', verbose_name='Заказ 2', on_delete=models.CASCADE, related_name='cutting_order_2', blank=True, null=True)
    order3 = models.ForeignKey('Productions', verbose_name='Заказ 3', on_delete=models.CASCADE, related_name='cutting_order_3', blank=True, null=True)
    order4 = models.ForeignKey('Productions', verbose_name='Заказ 4', on_delete=models.CASCADE, related_name='cutting_order_4', blank=True, null=True)
    order5 = models.ForeignKey('Productions', verbose_name='Заказ 5', on_delete=models.CASCADE, related_name='cutting_order_5', blank=True, null=True)
    order6 = models.ForeignKey('Productions', verbose_name='Заказ 6', on_delete=models.CASCADE, related_name='cutting_order_6', blank=True, null=True)

    def __str__(self):
        return (f'{self.format} \n '
                f'{self.order1} \n {self.order2} \n {self.order3} \n '
                f'{self.order4} \n {self.order5} \n {self.order6} \n')

    class Meta:
        db_table = 'cutting_cardboard'
        verbose_name = 'Раскрой'
        verbose_name_plural = 'Раскрой'
