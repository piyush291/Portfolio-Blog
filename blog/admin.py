from django.contrib import admin
from .models import post,Profile,Images,comment

# Register your models here.
# class postAdmin(admin.ModelAdmin):
#     list_display = ('title','slug','author','status')       #this is for display in admin panel

class postAdmin(admin.ModelAdmin):
    list_display = ('title','slug','author','status')   # the post is being displayed with 4 columns
    list_filter = ('slug','author','created')       # the filtering table given on right hand side
    search_fields = ['author__username','title']    # this gives us the searching menu
    list_editable = ('status',)     # this gives us the dropdown for changing of status
    date_hierarchy = ('created')     # jo table ke upar dates ke acc sort karne ki option aa rahi hai

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user','dob','photo')



class ImagesAdmin(admin.ModelAdmin):
    list_display = ('post1','image')




admin.site.register(post,postAdmin)
admin.site.register(Profile,ProfileAdmin)
admin.site.register(Images,ImagesAdmin)
admin.site.register(comment)


