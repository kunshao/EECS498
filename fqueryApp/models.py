from django.db import models

# Create your models here.
class status(models.Model):
    sid    = models.CharField(max_length = 12, primary_key = True)
    sfrom  = models.CharField(max_length = 30)
    smessage   = models.TextField()
    supdated_time  = models.DateTimeField("status updated time")

    def __unicode__(self):
        return self.smessage