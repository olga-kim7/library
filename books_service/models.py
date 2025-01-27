from django.db import models


class Book(models.Model):
    COVER_CHOISE = [
        ('HC', 'HARD'),
        ('SC', 'SOFT')
    ]

    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    cover = models.CharField(max_length=255, choices=COVER_CHOISE)
    inventory = models.PositiveIntegerField(default=0)
    daily_fee = models.DecimalField(max_digits=6, decimal_places=2, default=0)
