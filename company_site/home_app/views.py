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
    all_logs = reversed(all_logs)

    all_present_lists = []
    all_absent_lists = []
    for log in reversed(MeetingLog.objects.all()):
        present_list = ""
        absent_list = ""

        if log.arnav_present: present_list += "|  Arnav Rahman  |"
        else: absent_list += "|  Arnav Rahman  |"

        if log.kayden_present: present_list += "|  Kayden Hung  |"
        else: absent_list += "|  Kayden Hung  |"

        if log.ian_present: present_list += "|  Ian Wong  |"
        else: absent_list += "|  Ian Wong  |"

        if log.keon_present: present_list += "|  Keon Der  |"
        else: absent_list += "|  Keon Der  |"

        if log.bao_present: present_list += "|  Bao Tran  |"
        else: absent_list += "|  Bao Tran  |"

        if len(absent_list) == 0: absent_list += "None"

        all_present_lists.append(present_list)
        all_absent_lists.append(absent_list)

    combined_list = list(zip(all_logs, all_present_lists, all_absent_lists))

    return render(request, 'home_app/meeting_logs.html', {'combined_log_list': combined_list})