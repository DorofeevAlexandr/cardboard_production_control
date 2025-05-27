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
    name = models.CharField(max_length=40, unique=True)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        db_table = 'material'


class Order(UUIDMixin, TimeStampedMixin):
    name = models.CharField(max_length=40, unique=True)
    format = models.CharField(max_length=40)
    profile = models.CharField(max_length=40)
    material_outer = models.ForeignKey('Material', related_name='orders_material_outer', on_delete=models.CASCADE)
    material_corrugation = models.ForeignKey('Material', related_name='orders_material_corrugation', on_delete=models.CASCADE)
    material_inside = models.ForeignKey('Material', related_name='orders_material_inside', on_delete=models.CASCADE)

    def __str__(self):
        return (f'{self.name} - {self.format} - {self.profile} ({self.material_outer} {self.material_corrugation} '
                f'{self.material_inside})')

    class Meta:
        db_table = 'order'


class Productions(UUIDMixin, TimeStampedMixin):
    order_date = models.DateField()
    order = models.ForeignKey('Order', on_delete=models.CASCADE)
    quantity = models.IntegerField(validators=[MinValueValidator(0)])

    def __str__(self):
        return f'{self.order_date} - {self.order.__str__()} - {self.order} ({self.quantity})'

    class Meta:
        db_table = 'productions'
