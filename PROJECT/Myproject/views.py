from django.shortcuts import render

def index(request):
    return render(request, 'index.html')  # homepage template

def hostels(request):
    return render(request, 'hostels.html')  # hostels template
