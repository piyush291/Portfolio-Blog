from django.urls import path
from django.conf.urls import url
from blog import views

urlpatterns = [
    # path('',views.index,name='index'),
    path('datetime/',views.datetime,name='datetime'),
    path('',views.post_list,name='post_list'),
    # url(r'^(?P<id>\d+)/(?P<slug>[\w-]+)/$',views.post_details,name='post_details')
    path('<int:id>/',views.post_details,name='post_details'),
    path('<int:id>/post_delete',views.post_delete,name='post_delete'),
    path('<int:id>/post_favourite',views.post_favourite,name='post_favourite'),
    path('favourites/',views.post_favourite_list,name="post_favourite_list"),
    path('post_create/',views.post_create,name='post_create'),
    path('post_login/',views.user_login,name='user_login'),
    path('post_logout/',views.user_logout,name="user_logout"),
    path('post_register/',views.user_register,name="user_register"),
    path('post_edit_profile/',views.edit_profile,name="edit_profile"),
    path('<int:id>/edit_post/',views.edit_post,name="edit_post"),
    path('post_list/',views.post_list,name="post_list"),
    
]

