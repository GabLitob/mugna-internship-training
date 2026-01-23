from django.http import HttpResponse
from datetime import datetime, timedelta

def hello(request):
    return HttpResponse("Hello, world")

def current_datetime(request):
    now = datetime.datetime.now()
    html = "<html><body>It is now %s.</body></html>" % now
    return HttpResponse(html)

def hours_ahead(request, offset: int):
    future_time = datetime.now() + timedelta(hours=offset)
    return HttpResponse(f"In {offset} hour(s), it will be {future_time} into the future")