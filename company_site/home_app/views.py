from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from home_app.models import MeetingLog


def home_screen(request):
    return render(request, 'home_app/home_screen.html')

def crew(request):
    return render(request, 'home_app/crew.html')

def meeting_logs(request):
    all_logs = MeetingLog.objects.all()
    return render(request, 'home_app/meeting_logs.html', {'log_list': all_logs})