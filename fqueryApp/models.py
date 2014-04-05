from django.db import models

# Create your models here.
class status(models.Model):
    status_id		= models.CharField(max_length = 30, primary_key = True)
    status_from  	= models.CharField(max_length = 30)
    status_message	= models.TextField()
    status_time		= models.DateTimeField("status updated time")

    def __unicode__(self):
        return self.status_message
