from django.shortcuts import render
from .models import Issue

def home(request):
    return render(request, 'projects/issues.html', {})

def add_issue(request):
