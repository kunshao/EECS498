from django.db import models

# Create your models here.
class Status(models.Model):
    status_id               = models.CharField(max_length = 30, primary_key = True)
    status_from_id          = models.CharField(max_length = 30, blank=True)
    status_message          = models.TextField(blank = True)
    status_updated_time     = models.DateTimeField(blank = True, null = True)

    def __unicode__(self):
        return self.status_message


class Comment(models.Model):
    comment_id              = models.CharField(max_length = 30, primary_key = True)
    comment_from_id         = models.CharField(max_length = 30, blank=True)
    comment_message         = models.TextField(blank = True)
    comment_can_remove      = models.NullBooleanField(null = True)
    comment_created_time    = models.DateTimeField(blank = True, null = True)
    comment_like_count      = models.IntegerField(null = True)
    user_likes              = models.NullBooleanField(null = True)

    def __unicode__(self):
        return self.comment_message

class Photo(models.Model):
    photo_id              = models.CharField(max_length = 30, primary_key = True)
    photo_created_time     = models.DateTimeField(blank = True, null = True)
    photo_from_id         = models.CharField(max_length = 30, blank=True)
    photo_link = models.TextField(blank = True)
    photo_name = models.NullBooleanField(null = True)

    def __unicode__(self):
        return self.photo_name

