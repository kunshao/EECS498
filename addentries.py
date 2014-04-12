from fqueryApp.models import status
from django.utils import timezone

s0 = status(sid="0", sfrom="Shu", smessage="Tai Mai Shu", supdated_time=timezone.now())
s1 = status(sid="1", sfrom="Eyad", smessage="Okay, my Shu is Thai-ed", supdated_time=timezone.now())
s2 = status(sid="2", sfrom="Kun", smessage="What about my Shu?", supdated_time=timezone.now())

s0.save()
s1.save()
s2.save()