from django.shortcuts import redirect, render, get_object_or_404
from django.http import HttpResponse
from django.core.urlresolvers import reverse, reverse_lazy
from django.contrib import messages
from django.db.models import Count
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .forms import PostForm, CommentForm, LoginForm, UserRegistrationForm, UserEditForm, ProfileEditForm
from .models import Profile, Post
from pytz import timezone

# Create your views here.
def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'],
                               password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse('Authenticated successfully')
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login')
    else:
        form = LoginForm()
    return render(request, 'account/login.html', {'form': form})

def post_list(request):
    #if request.method == 'GET':
    #posts = Post.published.all()
    #return render(request, 'blog/index.html',
    #       {'posts': posts})
    object_list = Post.published.all()
    paginator = Paginator(object_list, 3) #7 posts per page
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        posts = paginator.page(paginator.num_pages)
    return render(request, 'blog/index.html',{'page': page, 'posts':posts})

def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post,
                             slug= post,
                             status='published',
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)
    #List of active comments for this post
    comments = post.comments.filter(active=True)
    if request.method == 'POST':
        # A comment was posted
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            #Create comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
            #Assign the current post to the comment
            new_comment.post = post
            #Save the comment to the database
            new_comment.save()
    else:
        comment_form = CommentForm()
    #List of similar posts
    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags', '-publish')[:4]
    return render(request,
                  'blog/detail.html',
                  {'post': post,
                   'comments': comments,
                   'comment_form': comment_form,
                   'similar_posts':similar_posts})

def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post= form.save(commit=False)
            post.author = request.user
            post.save()
            #return redirect(reverse_lazy('account:post_list'))
            return redirect('account:post_detail', post.publish.year, post.publish.strftime('%m'), post.publish.strftime('%d'), post.slug)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form, 'section': 'add_new'})
    
def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            #create a new user object but do not save it yet
            new_user = user_form.save(commit = False)
            #set the chosen password
            new_user.set_password(
                user_form.cleaned_data['password'])
            #Now save the user object
            new_user.save()
            #Create the user profile
            profile = Profile.objects.create(user=new_user)
            return render(request, 
                    'account/register_done.html', 
                    {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request,
            'account/register.html',
            {'user_form': user_form})
    
@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user,
                                data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile,
                                       data=request.POST,
                                       files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile updated successfully')
        else:
            messages.error(request, 'Error updating your profile')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    return render(request,'account/edit.html',
           {'user_form': user_form, 'profile_form': profile_form})
    
    
@login_required
def dashboard(request):  
    return render(request, 'account/dashboard.html',
                  {'section': 'dashboard'})    
    
    