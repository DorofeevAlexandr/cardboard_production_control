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
    # id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    id = models.AutoField(primary_key=True, editable=False)

    class Meta:
        abstract = True


class Density(UUIDMixin, TimeStampedMixin):
    density = models.IntegerField(verbose_name='Плотность, г/м²', default=100, validators=[MinValueValidator(0)])

    def __str__(self):
        return f'{self.density}'

    class Meta:
        db_table = 'density'
        verbose_name = 'Плотность материала'
        verbose_name_plural = 'Плотности материалов'


class Material(UUIDMixin, TimeStampedMixin):
    name = models.CharField(verbose_name='Материал', max_length=40)
    density = models.ForeignKey('Density', verbose_name='Плотность, г/м²', related_name='materials_density', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name}-{self.density}'

    class Meta:
        db_table = 'material'
        verbose_name = 'Материал слоя'
        verbose_name_plural = 'Материалы слоев'


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
    format = models.ForeignKey('Format', verbose_name='Формат, мм', related_name='orders_format', on_delete=models.CASCADE)
    profile = models.ForeignKey('Profile', verbose_name='Профиль', related_name='orders_profile', on_delete=models.CASCADE)
    material_outer = models.ForeignKey('Material', verbose_name='Наружный слой', related_name='orders_material_outer', on_delete=models.CASCADE)
    material_corrugation = models.ForeignKey('Material', verbose_name='Гофрирующий слой', related_name='orders_material_corrugation', on_delete=models.CASCADE)
    material_inside = models.ForeignKey('Material', verbose_name='Внутрений слой', related_name='orders_material_inside', on_delete=models.CASCADE)

    def __str__(self):
        return (f'{self.name} - {self.format} - {self.profile} ({self.material_outer} | {self.material_corrugation} | '
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
    order_status = models.IntegerField(choices=tuple(map(lambda x: (x[0], x[1]), Status.choices)),
                                       default=Status.IN_THE_QUEUE, verbose_name="Статус заказа")

    def __str__(self):
        return f'{self.order_date} - {self.order.__str__()} - {self.order} ({self.quantity}) ({self.order_status})'

    class Meta:
        db_table = 'productions'
        verbose_name = 'Сменное задание'
        verbose_name_plural = 'Сменные задания'

