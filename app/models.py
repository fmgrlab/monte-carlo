from django.db import models

class Hw_Step(models.Model):
    data = models.TextField()
    id = models.IntegerField(default=1, primary_key= True)


