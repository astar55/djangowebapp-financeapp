from django.db import models

# Create your models here.
'''Class that inherits from models.Model which has direct connection to db'''
class StockTicker(models.Model):
    stockname = models.CharField(max_length = 400)
    stockticker = models.CharField(primary_key = True, max_length = 200)
    