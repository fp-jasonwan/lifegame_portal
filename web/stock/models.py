from django.db import models

# Create your models here.
class Stock(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    lot_size = models.IntegerField()

class StockPrice(models.Model):
    stock = models.OneToOneField(StockBasic, verbose_name="股票", on_delete=models.CASCADE)