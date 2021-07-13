from django.shortcuts import render

# get home page overall
def GetHome(request):
    return render(request, 'home.html')