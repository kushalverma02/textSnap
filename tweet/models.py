from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class tweets(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(max_length=240)
    photo= models.ImageField(upload_to='photos/', blank = True , null = True)
    created_at = models.DateTimeField(auto_now_add=True)  
    updated_at = models.DateTimeField(auto_now = True)

    def __str__(self):
        return f'{self.user.username}-{self.text[:10]}'
    

#creating a model which is linked one to one to the user inbuilt model and having contact details 
class register_user(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    contact_number = models.IntegerField()
    profile_picture = models.ImageField(upload_to="profiles/%Y/%M/%D" , null = True , blank=True)
    gender = models.TextField(max_length=1 ,  null=True , blank=True)
    
    def __str__(self):
        return self.user.username