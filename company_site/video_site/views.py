from django.shortcuts import render
from django.contrib.auth import logout, get_user_model
from django.shortcuts import redirect
from user_forms import models

# Create your views here.
def landing_page(request):
    if request.user.is_authenticated:
        user = get_user_model().objects.get(id=request.user.id)
        user_settings = models.Settings.objects.get(user_key=user)

        # Render info if User is logged in
        account_info = [request.user.username, "Settings", "Logout"]
        account_links = ["javascript:;", "users/logout"]
        account_settings = [user_settings.max_age_restriction]
    else:
        # Render info if Guest Account is being used
        account_info = ["Guest", "Login", "Register"]
        account_links = ["users/login", "users/register"]
        account_settings = [1]

    return render(request, 'video_site/landing_page.html', 
                  {'ACCOUNT_INFO': account_info, 'ACCOUNT_LINKS': account_links, 'ACCOUNT_SETTINGS': account_settings})