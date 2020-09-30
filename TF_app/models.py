from django.db import models
from django.utils import timezone

# Create your models here.
class Project(models.Model):
    project_name = models.CharField(max_length=50)
    project_url = models.URLField()
    create_on = models.DateField(default=timezone.now)
    update_on = models.DateField(default=timezone.now,null=True,blank=True)
    upload_image = models.ImageField(upload_to='img/') 

    def __str__(self):
        return self.project_name

    



    

