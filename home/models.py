from django.db import models

# Create your models here.
class Media(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=300)
    url = models.URLField()
    credits = models.CharField(max_length=100, null=True, blank=True)
    date = models.DateField()
    media_id = models.CharField(max_length=200, null=True, blank=True, verbose_name="media_id (will get autofilled)")
    thumbnail = models.URLField(blank=True, null=True, max_length=400, verbose_name="Thumbnail (will get autofilled)")
    instagramIndex = models.IntegerField(blank=True, null=True, verbose_name="Index of instagram post (0 = most recent post) REQUIRED")

    def __str__(self):
        return (self.title + ' ' + str(self.date))

class Org(models.Model):
    name = models.CharField(max_length=30)
    description = models.TextField(max_length=100, blank=True)
    link=models.URLField()
    image = models.ImageField()

    def __str__(self):
        return self.name

class Photo(models.Model): #Must be 1280x720
    image = models.ImageField()
    order = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.image.name

    class Meta:
        ordering = ['order']
