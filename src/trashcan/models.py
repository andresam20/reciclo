from django.contrib.auth.models import User
from django.db import models


class TrashCan(models.Model):

    depth = models.FloatField(help_text='Profundidad del tacho.')
    barcode = models.CharField(
        max_length=100,
        null=True,
        blank=True,
    )
    lat = models.FloatField(
        null=True,
        blank=True,
    )
    lng = models.FloatField(
        null=True,
        blank=True,
    )
    address = models.CharField(
        max_length=300,
        null=True,
        blank=True,
    )

    recyclers = models.ManyToManyField(
        User,
        through='Harvest',
    )

    def __str__(self):
        return str(self.pk)

    class Meta:
        db_table = 'trash_can'


class Level(models.Model):

    trash_can = models.ForeignKey(
        TrashCan,
        related_name='levels',
    )
    time = models.DateTimeField(
        auto_now_add=True,
    )
    distance = models.FloatField(
        help_text='Distancia del sensor a la basura (cm).'
    )

    def __str__(self):
        return str(self.pk)

    class Meta:
        db_table = 'level'


class Harvest(models.Model):

    user = models.ForeignKey(User)
    trash_can = models.ForeignKey(TrashCan)
    date = models.DateField()

    STATUS = (
        (0, 'Por recoger'),
        (1, 'Trabajo hecho'),
    )
    status = models.BooleanField(
        max_length=50,
        choices=STATUS,
        default=0,
    )
    comment = models.TextField(
        blank=True,
        null=True,
    )

    def __str__(self):
        return str(self.pk)

    class Meta:
        db_table = 'harvest'
        unique_together = ('user', 'trash_can', 'date')
