from django.http import HttpResponse
from datetime import datetime
dtnow = datetime.now()

def index(request):
    return HttpResponse("Hello World")

def date(request):
    return HttpResponse(dtnow)