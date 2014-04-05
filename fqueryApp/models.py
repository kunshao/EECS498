from django.db import models

# Create your models here.
class Status(models.Model):
    status_id               = models.CharField(max_length = 30, primary_key = True)
    status_from_id          = models.CharField(max_length = 30, null = True)
    status_message          = models.TextField(null = True)
    status_updated_time     = models.DateTimeField(null = True)

    def __unicode__(self):
        return self.status_message
