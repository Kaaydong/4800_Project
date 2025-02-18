from django.shortcuts import render
from django.contrib.auth import logout
from django.shortcuts import redirect

# Create your views here.
def landing_page(request):
    if request.user.is_authenticated:
        # Render info if User is logged in
        account_info = [request.user.username, "Settings", "Logout"]
        account_links = ["#", "users/logout"]
    else:
        # Render info if Guest Account is being used
        account_info = ["Guest", "Login", "Register"]
        account_links = ["users/login", "users/register"]

    return render(request, 'video_site/landing_page.html', {'ACCOUNT_INFO': account_info, 'ACCOUNT_LINKS': account_links})