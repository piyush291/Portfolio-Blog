from django.db import models

# Create your models here.

class memories(models.Model):
    img = models.ImageField(upload_to=None, height_field=None, width_field=None, max_length=None) # isme id col banane ki zaroorat nahi hai automaticaly bana dega 

    # img: str   yeh tab use karna hai jab database se link nahi karna aur manualy images add karni hai


class comment(models.Model):
    pass
