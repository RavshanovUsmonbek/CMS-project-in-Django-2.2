from django.contrib.auth.models import User
from math import ceil
from django.shortcuts import render
from cms_app.models import Catagory,UserProfile,Comment,Post
from cms_app.forms import CommentForm, CategoryForm, EditPostForm, AddPostForm, RegisterUserForm, RegisterUserProfileForm, EditUserProfile
from django.db.models import Q
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.http import HttpResponseRedirect, HttpResponse
from django.core.paginator import Paginator
# Create your views here.

def index(request):
    posts_per_page =2
    catagories = Catagory.objects.all().order_by('cat_title')
    cat_half =ceil(catagories.count()/2)
    cat_first_half = catagories[0:cat_half]
    cat_second_half = catagories[cat_half:catagories.count()]
    posts = Post.objects.filter(post_status='published')[0:posts_per_page]
    count = ceil(Post.objects.filter(post_status='published').count()/posts_per_page)

    if 'page' in request.GET:
        page = int(request.GET['page'])
        posts = Post.objects.filter(post_status='published')[(page-1)*posts_per_page:(page)*posts_per_page]

    if 'search' in request.POST:
        search_item = request.POST['search']
        posts = Post.objects.filter(Q(post_title__icontains = search_item)|
                                    Q(post_content__icontains = search_item)|
                                    Q(post_tags__icontains = search_item))

    post_list = Post.objects.filter(post_status='published')
    paginator = Paginator(post_list,posts_per_page)
    page = request.GET.get('page')
    contacts = paginator.get_page(page)

    dict ={
        'catagories':catagories,
        'cat_first_half':cat_first_half,
        'cat_second_half':cat_second_half,
        'posts':posts,
        'range':range(1,count+1),
        'contacts':contacts,
    }

    return render(request,'cms_app/index.html',dict)

def sort(request, cat_id):
        catagories = Catagory.objects.all().order_by('cat_title')
        posts = Post.objects.filter(post_cat_id = cat_id,post_status='published')
        cat_half =ceil(catagories.count()/2)
        cat_first_half = catagories[0:cat_half]
        cat_second_half = catagories[cat_half:catagories.count()]



        dict ={
                'catagories':catagories,
                'cat_first_half':cat_first_half,
                'cat_second_half':cat_second_half,
                'posts':posts,
        }
        return render(request,'cms_app/index.html',dict)

def post_sort(request, by, id):
    if by == 'author':
        posts = Post.objects.filter(post_author = id)

    dict = {'posts':posts}

    return render(request,'cms_app/index.html',dict)

def register(request):

    if request.POST:
        UserForm = RegisterUserForm(request.POST)
        ProfileForm =RegisterUserProfileForm(request.POST, request.FILES)

        if UserForm.is_valid() and ProfileForm.is_valid():
            user=UserForm.save()
            user.set_password(user.password)
            user.save()

            profile=ProfileForm.save(commit=False)
            profile.user = user

            if 'user_image' in request.FILES:
                profile.user_image = request.FILES['user_image']

            profile.save()
            return redirect('cms_app:admin_index')
    else:
        UserForm = RegisterUserForm()
        ProfileForm = RegisterUserProfileForm()
    return render(request, 'cms_app/registration.html', {'form':UserForm,'form_profile':ProfileForm,})


def post(request, id):
    catagories = Catagory.objects.order_by('cat_title')
    post = Post.objects.get(post_id=id)
    comments = Comment.objects.filter(com_post_id=id, com_status = 'approved')
    commentForm = CommentForm()
    warning = "None"

    if request.method=="POST":
        if request.user.is_authenticated:
            commentForm = CommentForm(request.POST)
            if commentForm.is_valid():
                comment = commentForm.save(commit=False)
                comment.com_author = request.user
                comment.com_post_id = post
                comment.com_status = 'disapproved'
                comment.save()
                post.post_comment_count = post.post_comment_count+1;
                post.save()
        else:
            warning = "Only signed users can comment"

    commentForm = CommentForm()
    dict ={
        'catagories':catagories,
        'post':post,
        'comments':comments,
        'commentForm':commentForm,
        'warning':warning
        }

    return render(request,'cms_app/post.html',dict)

@login_required(login_url='/login/')
def admin_index(request):
    dict={}
    if request.session.has_key('user_id'):

        user_id = request.session['user_id']
        user = User.objects.get(pk=user_id)
        user_count = User.objects.all().count()
        com_count = Comment.objects.all().count()
        cat_count = Catagory.objects.all().count()
        post_count = Post.objects.all().count()
        active_post_count = Post.objects.filter(post_status = 'published').count()
        draft_post_count = Post.objects.filter(post_status = 'unpublished').count()
        pending_comments = Comment.objects.filter(com_status = 'disapproved').count()
        subscribers_count = UserProfile.objects.filter(user_isAdmin=False).count()

        dict = {
            'user':user,
            'user_count':user_count,
            'post_count':post_count,
            'com_count':com_count,
            'cat_count':cat_count,
            'zipped_data':{'Active posts':active_post_count,
                            'Draft posts':draft_post_count,
                            'Comments':com_count,
                            'Pending comments':pending_comments,
                            'Users':user_count,
                            'Subscribers':subscribers_count,
                            'Categories':cat_count},
        }

    return render(request,'admin/admin_index.html',dict)

@login_required(login_url='/login/')
def admin_category(request):
    form = CategoryForm()
    categories = Catagory.objects.all()

    if request.method=='POST':
        form = CategoryForm(request.POST)

        if form.is_valid():
            form.save(commit =True)

    return render(request,'admin/category.html',{'form':form, 'categories':categories,})

@login_required(login_url='/login/')
def cat_delete(request,id):
    Catagory.objects.get(pk=id).delete()
    categories = Catagory.objects.all()
    form = CategoryForm()
    return render(request,'admin/category.html',{'form':form, 'categories':categories,})

@login_required(login_url='/login/')
def cat_edit(request,id):
    updating_cat = Catagory.objects.get(pk=id)
    categories = Catagory.objects.all()
    form = CategoryForm()

    if request.method == "POST":
        value = request.POST['cat_title']
        updating_cat.cat_title = value;
        updating_cat.save()

    dict ={
        'form':form,
        'categories':categories,
        'updating_cat':updating_cat,
    }

    return render(request,'admin/category.html',dict)

@login_required(login_url='/login/')
def admin_post(request):
    posts = Post.objects.all()
    dict = {'posts':posts,}
    return render(request,'admin/post.html',dict)

@login_required(login_url='/login/')
def post_delete(request,id):
    Post.objects.get(pk=id).delete()
    return redirect('cms_app:post')

    return admin_post(request)

@login_required(login_url='/login/')
def post_edit(request,id):
    updating_post = Post.objects.get(pk=id)
    form = EditPostForm(instance = updating_post)

    if request.method == "POST":
        form = EditPostForm(request.POST, request.FILES, instance = updating_post)
        if form.is_valid():
            form.save()
            # updating_post.post_image = request.POST['post_image']
            # updating_post.save()
            print("SAVED")
            return redirect('cms_app:post')
        else:
            print("ERROR! INVALID DATA")

    return render(request,'admin/post_edit.html',{'updating_post':updating_post,'form':form})

@login_required(login_url='/login/')
def post_add(request):
    if request.method =="POST":
        form = AddPostForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            if request.POST['submit'] == 'SR':
                return redirect('cms_app:post')
            elif request.POST['submit']=='SA':
                return redirect('cms_app:post_add')
        else:
            print("INVALID DATA inserted")
    else:
        form = AddPostForm()
        dict ={'form':form,}
        return render(request, 'admin/post_add.html', dict)

@login_required(login_url='/login/')
def comment(request):
    comments = Comment.objects.all()
    return render(request,'admin/admin_comments.html',{'comments':comments})

@login_required(login_url='/login/')
def comment_delete(request,id):
    Comment.objects.get(pk=id).delete()
    return redirect('cms_app:comment')

@login_required(login_url='/login/')
def comment_approval(request,id,status):
    com =Comment.objects.get(pk=id)
    com.com_status = status
    com.save()
    return redirect('cms_app:comment')

@login_required(login_url='/login/')
def users(request):
    users = User.objects.all()
    return render(request,'admin/allusers.html',{'users':users})

@login_required(login_url='/login/')
def user_add(request):
    if request.POST:
        UserForm = RegisterUserForm(request.POST)
        ProfileForm =RegisterUserProfileForm(request.POST, request.FILES)

        if UserForm.is_valid() and ProfileForm.is_valid():
            user=UserForm.save()
            user.set_password(user.password)
            user.save()

            profile=ProfileForm.save(commit=False)
            profile.user = user

            if 'user_image' in request.FILES:
                profile.user_image = request.FILES['user_image']

            profile.save()

            if request.POST['submit'] == 'SR':
                return redirect('cms_app:SeeUsers')
            elif request.POST['submit']=='SA':
                return redirect('cms_app:user_add')
    else:
        UserForm = RegisterUserForm()
        ProfileForm = RegisterUserProfileForm()

    return render(request, 'admin/user_add.html', {'form':UserForm,'form_profile':ProfileForm,})

@login_required(login_url='/login/')
def user_role(request, id, isAdmin):
    user = UserProfile.objects.get(pk=id)
    user.user_isAdmin =isAdmin
    user.save()
    return redirect('cms_app:SeeUsers')

@login_required(login_url='/login/')
def user_delete(request, id):
    User.objects.get(pk=id).delete()
    return redirect('cms_app:SeeUsers')

@login_required(login_url='/login/')
def user_profile(request):

    if request.session.has_key('user_id'):
        user_id = request.session['user_id']
        user1 = User.objects.get(pk=user_id)

        if request.POST:
            UserForm = RegisterUserForm(request.POST, instance=user1)
            ProfileForm = EditUserProfile(request.POST, request.FILES, instance=user1.userprofile)

            if UserForm.is_valid() and ProfileForm.is_valid():
                user=UserForm.save()
                user.set_password(user.password)
                user.save()
                update_session_auth_hash(request, user)

                profile=ProfileForm.save(commit=False)
                profile.user = user

                if 'user_image' in request.FILES:
                    profile.user_image = request.FILES['user_image']

                profile.save()
                return redirect('cms_app:user_profile')
        else:
            UserForm = RegisterUserForm(instance=user1)
            ProfileForm = EditUserProfile(instance=user1.userprofile)

    else:
        return redirect('cms_app:user_login')

    return render(request,'admin/user_profile.html',{'user':user1,'form':UserForm, 'form_profile':ProfileForm})


def user_login(request):
    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username,password=password)

        if user:
            if user.is_active:
                login(request, user)
                request.session['user_id'] = user.id
                return redirect('cms_app:admin_index')
            else:
                return HttpResponse("YOUR ACCOUNT IS NOT ACTIVE")
        else:
            return HttpResponse("INVALID Details are supplied")
    elif request.GET['next']:
        return render(request,'cms_app/login.html',{})
    else:
        return render(request,'cms_app/index.html',{})

@login_required
def user_logout(request):
    # Log out the user.
    del request.session['user_id']
    logout(request)
    # Return to homepage.
    return redirect('cms_app:index')
