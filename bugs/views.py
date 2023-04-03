from django.shortcuts import get_object_or_404, redirect, render
from profiles.models import UserProfile
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import urllib
import os
import requests

# Create your views here.

@login_required
def bug(request):

    profile = get_object_or_404(UserProfile, user=request.user)

    if request.method == "POST":
        data = request.body.decode('ascii', 'replace')
        raw_title = data.split('title=')[1].split('&bug-text')[0]
        title = urllib.parse.unquote(raw_title, encoding='utf-8', errors='replace').replace("+", " ")
        raw_bug_text = data.split('bug-text=')[1]
        bug_text = urllib.parse.unquote(raw_bug_text, encoding='utf-8', errors='replace').replace("+", " ")
        
        owner = os.environ.get('GITHUB_OWNER')
        token = os.environ.get('GITHUB_TOKEN')
        repo = os.environ.get('GITHUB_REPO')
        url = f'https://api.github.com/repos/{ owner }/{ repo }/issues'
        payload = {'title': f'{request.user}: {title}', 'body': bug_text}

        response = requests.post(url, auth=(owner, token), json=payload)
        if response.status_code == 201:
            messages.success(request, 'Bug successfully reported.')
            return redirect('dashboard')
        else:
            messages.error(request, 'Unable to report bug, please try again later.')
            return redirect('dashboard')

    context = {
        'profile': profile,
        'title': 'Pioneer Partner - Report a Bug',
    }

    return render(request, 'bugs/bug.html', context)