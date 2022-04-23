from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.conf import settings
from django.contrib.auth.models import User
# Create your models here.
#guest -- movie -- reserstion
class Movie(models.Model):
    hall=models.CharField(max_length=10)
    movie=models.CharField(max_length=200)
    date=models.DateField( )
    def __str__(self):
        return str(self.movie)
class Guest(models.Model):
    name=models.CharField(max_length=100,blank=True,default='custmer')
    phone=models.CharField(max_length=20,blank=True,default='No Avalble data')
    def __str__(self):
        return str(self.pk)

class Reservation(models.Model):
    guest=models.ForeignKey(Guest,related_name='Guest_Reservation',on_delete=models.CASCADE)
    movie=models.ForeignKey(Movie,related_name='Guest_Reservation',on_delete=models.CASCADE)
    def __str__(self):
        return str(self.movie)+' & '+str(self.movie)

class Post(models.Model):
    auther=models.ForeignKey(User,on_delete=models.CASCADE)
    tilte=models.CharField(max_length=50)#فيه ايرور ف اتايتيل ومكسل اعدله 
    body=models.TextField(max_length=150)
    def __str__(self):
        return self.tilte

@receiver(post_save ,sender=settings.AUTH_USER_MODEL)
def TokenCreate(sender,instance,created,**kwargs):
    if created:
        Token.objects.create(user=instance)