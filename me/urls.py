from django.urls import path

from . import views

urlpatterns = [
    path('',views.index,name='home'),
    path('project1.html',views.index),
    path('contact.html',views.contact,name='contact'),
    path('saic.html',views.saic,name='saic'),
    path('modelling.html',views.modelling,name='modelling'),
    path('academics.html',views.academics,name='academics'),
    path('sports.html',views.others)
]
