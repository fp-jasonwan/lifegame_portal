from django.db import models

# Create your models here.
class NewsCategory(models.Model):
    def __str__(self):
        return self.name
        
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)

class News(models.Model):
    id = models.AutoField(primary_key=True)
    category_id = models.OneToOneField(NewsCategory, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    message = models.TextField(max_length=200)
    date = models.DateField()
    time = models.TimeField()