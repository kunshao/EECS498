from django.db import models

# Create your models here.
class Status(models.Model):
    status_id               = models.CharField(max_length = 30, primary_key = True)
    status_from_id          = models.CharField(max_length = 30, blank=True)
    status_message          = models.TextField(blank = True)
    status_updated_time     = models.DateTimeField(blank = True, null = True)

    def __unicode__(self):
        return self.status_message
