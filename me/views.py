from django.shortcuts import render
from .models import memories

# Create your views here.

def index(request):
    return render(request,'project1.html')


def contact(request):
    if request.method== 'POST':
        comment=request.POST['comment']
    return render(request,'contact.html')


def saic(request):

    # obj1=memories()
    # obj1.img='static/img/1.jpg'

    # obj2=memories()
    # obj2.img='static/img/2.jpg'

    # obj3=memories()
    # obj3.img='static/img/5.jpg'

    # objs=[obj1, obj2, obj3]

    objs = memories.objects.all()
    return render(request,'saic.html',{'objs': objs})


def modelling(request):
    return render(request,'modelling.html')

def academics(request):
    return render(request,'academics.html')

def others(request):
    return render(request,'others.html')