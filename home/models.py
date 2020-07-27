from django.db import models
# Create your models here.
class Contact(models.Model):
    sno = models.AutoField(primary_key=True)
    name= models.CharField(max_length=200)
    email= models.CharField(max_length=200)
    phone= models.CharField(max_length=50)
    Disc=models.CharField(max_length=1000)
    timestamp =models.DateTimeField(auto_now_add=True, blank= True)

    def __str__(self):
        return self.name

class UserProfile(models.Model):
  name= models.CharField(max_length=50)
  pic= models.ImageField(upload_to='images')

  def __str__(self):
        return self.names