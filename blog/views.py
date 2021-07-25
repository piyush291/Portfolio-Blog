from django.shortcuts import render,get_object_or_404,redirect
from django.http import HttpResponse,HttpResponseRedirect , JsonResponse,Http404
from django.utils import timezone
from .models import post,Profile,Images,comment
from .forms import *
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib.auth.models import auth,User
from django.db.models import Q
# from haystack.utils.highlighting import Highlighter
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger 
from django.template.loader import render_to_string
from django.forms import modelformset_factory
from django.contrib import messages


# Create your views here.
def index(request):
    return HttpResponse("hello i am piyush , present time is %s, %datetime.now()")

def datetime(request):
    #ret = "<html><body> present time is %s,  </body></html>" % datetime.datetime.date()
    # ret1=datetime.datetime.now()
    ret1 = timezone.now()
    return HttpResponse(ret1)

def post_list(request):
    # posts = post.objects.all()
    # if we write here post.published.all() -- then only with status published will be shown
    post_list = post.objects.all().order_by('-id')
    query=request.GET.get('q')

    if query:
        print("heloooooooooooooooooooooooooooooo")
        print(query)
        # posts = post.objects.filter(
        post_list = post.objects.filter(
            Q(title__icontains=query)|
            Q(author__username=query)|
            Q(body__icontains=query)
        )
    # highlight=Highlighter(query)
    # highlight.highlight(posts)
    paginator = Paginator(post_list, 10)   # here we have to specify how maby post we want to view per page
    page=request.GET.get('page')
    # posts = paginator.get_page(page)
    try:
        posts=paginator.page(page)
    except EmptyPage:
        posts=paginator.page(1)
    except PageNotAnInteger:
        posts=paginator.page(paginator.num_pages)


    if page is None:    # this is when initially user has not chosen any page, then 1-7 will be shown
        start_index = 0
        end_index = 7
    else:
        (start_index, end_index) = proper_pagination(posts,index=4)

    page_range = list(paginator.page_range)[start_index:end_index]   # this is the range of pages to be shown.

    context={
        'posts': posts,
        'page_range':page_range
    }

    return render(request,'post_list.html',context)


def proper_pagination(posts,index):
    start_index=0
    end_index=7
    if posts.number > index:               # means the change has to be made after page 5
        start_index = posts.number - index
        end_index = start_index + end_index
    return (start_index,end_index) 


def post_details(request,id):
    # post1 = post.objects.get(id=id)
    post1 = get_object_or_404(post,id=id)
    comments=comment.objects.filter(post1=post1,reply=None).order_by('-id')
    is_liked=False
    is_favourite=False 
    if post1.likes.filter(id=request.user.id).exists():
        is_liked=True

    if post1.favourite.filter(id=request.user.id).exists():
        is_favourite=True


    if request.method =='POST':
        comment_form=commentForm(request.POST or None)
        print("if ke andar")
        if comment_form.is_valid():
            print("valid ho gaya")
            content=request.POST.get('content')
            print("yeh content ki value hai",content)
            reply_id=request.POST.get('comment_id')    # reply_id should get comment.id
            print("yeh reply_id ki value hai",reply_id)
            comment_qs=None
            if reply_id:
                print("doosre if ke andar")
                comment_qs=comment.objects.get(id=reply_id)
                print(comment_qs)


            comment1=comment.objects.create(post1=post1,user=request.user,content=content,reply=comment_qs)
            comment1.save()
            print("save ho gaya")
            return HttpResponseRedirect(post1.get_absolute_url())
    else:
        print("pehle")
        comment_form=commentForm()
    

    context = {
        'post1': post1,
        'is_liked':is_liked,
        'is_favourite':is_favourite,
        'total_likes':post1.total_likes(),
        'comments':comments,
        'comment_form':comment_form,
    }
    
    return render(request,'post_details.html', context)
    # return reverse('post_details')

def post_create(request):
    ImageFormset= modelformset_factory(Images, fields=('image',), extra= 4, max_num= 4)  # agar ek se zyada images ki input leni hai toh extra=4 likhna hai
    form=None
    if request.method =='POST':
        form=PostCreateForm(request.POST)
        formset = ImageFormset(request.POST or None,request.FILES or None)
        if form.is_valid() and formset.is_valid():
            post=form.save(commit=False)
            post.author=request.user
            post.save()

            for f in formset:
                try:
                    print("try ke andar")
                    photo= Images(post1=post,image=f.cleaned_data['image'])
                    photo.save()
                    print("save ho gayi hogi")
                    # return redirect("{% url 'post_list.html' %}")
                    # return render(request,'post_list.html')
                    #return redirect('post_list')
                except:
                    print("post_create ka except")
                    break
            print("doosra waala")
            # return redirect("{% url 'post_list.html' %}")
            # return render(request,'post_list.html')
            messages.success(request,"post has been successfully created")
            return redirect('post_list')

    else:
        form=PostCreateForm()
        formset=ImageFormset(queryset=Images.objects.none())
    context = {
        'form':form,
        'formset':formset,
    }
    return render(request,'post_create.html',context)



def post_favourite_list(request):
    user=request.user
    favourite_post=user.favourite.all()
    context={
        'favourite_post':favourite_post,
    }
    return render(request,'post_favourite_list.html',context)

def post_favourite(request,id):
    post1 = get_object_or_404(post,id=id)
    if post1.favourite.filter(id=request.user.id).exists():
        post1.favourite.remove(request.user)
    else:
        post1.favourite.add(request.user)
    return HttpResponseRedirect(post1.get_absolute_url())



def post_like(request):
    post1 = get_object_or_404(post,id=request.POST.get('post_id'))
    is_liked=False
    if post1.likes.filter(id=request.user.id).exists():
        post1.likes.remove(request.user)
        is_liked=False
    else:
        is_liked=True
        post1.likes.add(request.user)
        
    context ={                          # this has to be included only when using ajax
        'post1': post1,
        'is_liked':is_liked,
        'total_likes':post1.total_likes()
    }

    if request.is_ajax():
        html=render_to_string('post_like.html',context, request=request)
        return JsonResponse({'form':html})
    # return HttpResponseRedirect(post1.get_absolute_url())     -- this will be written while not using jsonResponse
    



 # ----------------------------------------------------------------

def user_login(request):
    form=None
    if request.method =='POST':
        form=UserLoginForm(request.POST)
        if form.is_valid():
            username=request.POST['username']
            password=request.POST['password']
            user=authenticate(username=username,password=password)
            if user:
                if user.is_active:
                    login(request,user)
                    return HttpResponseRedirect(reverse('post_list'))
                else:
                    return HttpResponse("user is not active")
            else:
                print('views ke andar user_login mein')
                return HttpResponse("user is none")
    else:
        form=UserLoginForm()

    context={
        'form':form
    }
    return render(request,'post_login.html',context)


#------------------------------------------------------------------------------------------------------


def user_logout(request):
    auth.logout(request)
    return redirect ('post_list')

# --------------------------------------------------------------------------------------------

def user_register(request):
    form=None
    if request.method =="POST":
        print("views mein")
        form=UserRegistrationForm(request.POST)
        if form.is_valid():
            print('chal raha hai')
            new_user=form.save()
            new_user.set_password(form.cleaned_data['password'])
            # new_user=User.objects.create_user()
            new_user.save()
            Profile.objects.create(user=new_user)
            return redirect('post_list')
    else:
        print("else waala part")
        form=UserRegistrationForm()
    context={
        'form' : form
    }
    print("idhar bhi")
    return render(request,'post_register.html',context)


#-------------------------------------------------------------------------------



@login_required
def edit_profile(request):
    if request.method == "POST":
        user_form = UserEditForm(data=request.POST or None , instance= request.user)  # instance is used for getting the previous filled data
        profile_form = ProfileEditForm(data=request.POST or None,instance= request.user.profile,files=request.FILES)  # this is particularly for images
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return HttpResponseRedirect(reverse('edit_profile'))
    else:
        user_form = UserEditForm(instance= request.user)
        profile_form = ProfileEditForm(instance= request.user.profile)
    
    context={
        'user_form': user_form,
        'Profile_form': profile_form
    }  

    return render(request,'post_edit_profile.html',context)

# ---------------------------------------------------------------------------------



def edit_post(request,id):
    post1 = get_object_or_404(post,id=id)
    ImageFormset= modelformset_factory(Images, fields=('image',), extra= 4, max_num= 4)
    post_form=None
    if request.method == "POST":
        post_form = PostEditForm(data=request.POST or None , instance=post1)  # instance is used for getting the previous filled data
        formset = ImageFormset(request.POST or None,request.FILES or None)
        # profile_form = ProfileEditForm(data=request.POST or None,instance= request.user.profile,files=request.FILES)  # this is particularly for images
        if post_form.is_valid() and formset.is_valid():
            post_form.save()
            print(formset.cleaned_data,"PIYUSH")



            data=Images.objects.filter(post1=post1)            # this was used while updating the images
            for index, f in enumerate(formset):
                if f.cleaned_data:
                    print("itni baar")
                    if f.cleaned_data['id'] is None:
                        photo= Images(post1=post1,image=f.cleaned_data['image'])
                        photo.save()

                    elif f.cleaned_data['image'] is False:
                        print("andar aa gaya")
                        photo=Images.objects.get(id=request.POST.get('form-' + str(index) + '-id'))
                        photo.delete()

                    else:
                        photo= Images(post1=post1,image=f.cleaned_data['image'])
                        d=Images.objects.get(id=data[index].id)
                        d.image=photo.image
                        d.save()



            # for f in formset:                            # this is used when to store images
                #if f.cleaned_data:
                   # print("itni baar")
                    # if f.cleaned_data['id'] is None:
                        # photo= Images(post1=post1,image=f.cleaned_data['image'])
                        #photo.save()
                        # profile_form.save()
            messages.success(request, "{} has been successfully updated".format(post1.title) )
            return HttpResponseRedirect(post1.get_absolute_url())
    else:
        post_form = PostEditForm(instance=post1)
        formset=ImageFormset(queryset=Images.objects.filter(post1=post1))
        # profile_form = ProfileEditForm(instance= request.user.profile)
    
    context={
        'post_form': post_form,
        'post1':post1,
        'formset' : formset,
        # 'Profile_form': profile_form
    }  
    print("yahin dikkat aa arahai hai")
    print()
    print()
    print()
    return render(request,'edit_post.html',context)


def post_delete(request,id):
    post1=get_object_or_404(post,id=id)
    if request.user != post1.author:
        raise Http404()
    post1.delete()
    messages.warning(request, "{} post has been successfully delete".format(post1.title))
    return redirect('post_list')


