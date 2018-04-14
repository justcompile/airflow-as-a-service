from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import JsonResponse

from github import Github


@login_required
def home(request):
    return render(request, 'account/home.html')