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


class Link(models.Model):
    link_id                 = models.CharField(max_length = 30, primary_key = True)
    link_created_time       = models.DateTimeField(blank = True, null = True)
    link_description        = models.TextField(blank = True)
    link_from_id            = models.CharField(max_length = 30, blank=True)
    link_icon               = models.TextField(blank = True)
    link_link               = models.TextField(blank = True)
    link_message            = models.TextField(blank = True)
    link_name               = models.TextField(blank = True)
    link_picture            = models.TextField(blank = True)

    def __unicode__(self):
        return self.link_name

class Photo(models.Model):
    photo_id                = models.CharField(max_length = 30, primary_key = True)
    photo_created_time      = models.DateTimeField(blank = True, null = True)
    photo_from_id           = models.CharField(max_length = 30, blank=True)
    photo_link              = models.TextField(blank = True)
    photo_name              = models.TextField(blank = True)

    def __unicode__(self):
        return self.photo_name

class Note(models.Model):
    note_id                 = models.CharField(max_length = 30, primary_key = True)
    note_created_time       = models.DateTimeField(blank = True, null = True)
    note_from_id            = models.CharField(max_length = 30, blank=True)
    note_message            = models.TextField(blank = True)
    note_subject            = models.TextField(blank = True)
    note_updated_time       = models.DateTimeField(blank = True, null = True)

    def __unicode__(self):
            return self.note_subject

class Video(models.Model):
    video_id                = models.CharField(max_length = 30, primary_key = True)
    video_created_time      = models.DateTimeField(blank = True, null = True)
    video_description       = models.TextField(blank = True)
    video_embed_html        = models.TextField(blank = True)
    video_from_id           = models.CharField(max_length = 30, blank=True)
    video_name              = models.TextField(blank = True)
    video_source            = models.TextField(blank = True)
    video_updated_time      = models.TextField(blank = True)

    def __unicode__(self):
            return self.video_name

