from django.db import models

# Create your models here.

class Tag(models.Model):
    tag_name = models.CharField(max_length=32)
    def __str__(self):
         return self.tag_name

class Image(models.Model):
     fake_id = models.IntegerField(default=0)
     image_path = models.ImageField(upload_to="")
     image_tags = models.ManyToManyField(Tag)
     thumbnail_path = models.ImageField(upload_to="thumbnails/", default=None)
     def __str__(self):
          return str(self.fake_id)
     
class CommutationTable(models.Model):
     image_id = models.IntegerField()
     tag_id = models.IntegerField()
     def __str__(self):
          return (str(self.image_id) + ' ' + str(self.tag_id))