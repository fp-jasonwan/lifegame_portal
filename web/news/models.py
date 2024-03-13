from django.db import models

# Create your models here.
class NewsCategory(models.Model):
    def __str__(self):
        return self.name
        
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, unique=True)

class News(models.Model):
    id = models.AutoField(primary_key=True)
    category = models.ForeignKey(NewsCategory, related_name='news_category',
        on_delete=models.CASCADE, 
        null=True, blank=True)
    title = models.CharField(max_length=100)
    message = models.TextField(max_length=200)
    # image_url = models.TextField(max_length=1000, blank=True, null=True)
    image = models.ImageField(upload_to ='uploads/', blank=True, null=True) 
    date = models.DateTimeField(verbose_name='發怖時間')