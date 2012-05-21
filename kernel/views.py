from django.shortcuts import render_to_response
# Create your views here.

def one_day(request):
    return render_to_response('one_day.html')
