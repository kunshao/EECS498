import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "fquery.settings")
from django.conf import settings

from fqueryApp.models import Status
import fqueryApp.queryProcess

stopwords = fqueryApp.queryProcess.importStopwords()

# for testing purposes
query = raw_input("query:")



query = query.lower()
words = query.split()

# query_set is the set of results to be returned
query_set = Status.objects.none()
for word in words:
    if word in stopwords:
        continue
    word = fqueryApp.queryProcess.stemword(word)
    query_set = query_set| Status.objects.filter(status_message__contains = word)

for status in query_set:
    item = status.status_message
    tokens = fqueryApp.queryProcess.processLine(item)
    print status