from django.db import models

# Create your models here.
class Users(models.Model):
    # email = models.EmailField()
    phone = models.CharField(max_length=20)
    name = models.TextField()
    pwd = models.TextField()
    # dob = models.CharField(max_length=100)
    age = models.CharField(max_length=3)
    
    status = models.IntegerField()  
    mode = models.CharField(max_length=1) #p - normal; t - technician; d - doctor

class Results(models.Model):
    rid = models.TextField()
    phone = models.CharField(max_length=20)
    date = models.CharField(max_length=100)
    result = models.IntegerField() #value is 1 if positive else 0

    heart = models.CharField(max_length=10)
    lung = models.CharField(max_length=10)
    ratio = models.CharField(max_length=10)
    # url = models.TextField()
    dPhone = models.CharField(max_length=20)
    pPhone = models.CharField(max_length=20)
    # pName = models.CharField(max_length=101)
    # pAge = models.IntegerField()
    # pContact = models.IntegerField()
    pNotes = models.TextField()

class Images(models.Model):
    rid = models.TextField()
    image = models.ImageField(upload_to='xrayData/')
    # newResult = models.IntegerField()
    #do you think the result is wrong? -> collect result from user -> save the value -> retrain new data