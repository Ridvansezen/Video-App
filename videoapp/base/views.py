from django.shortcuts import render

def home_page(request):
    return render(request, "index.html")


def explore_page(request):
    return render(request, "explore.html")
