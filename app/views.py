from django.shortcuts import render, redirect, HttpResponse,HttpResponseRedirect, get_object_or_404, reverse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.contrib.auth.models import User
from .models import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
import datetime
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from .forms import *
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from django.contrib.auth.models import User
from django.contrib import auth
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
# Create your views here.


def section(request, pk):
    community = Section.objects.get(id=pk)
    g = community.post_set.order_by("-created_on")
    if request.method == 'POST':
        if request.user.is_authenticated:
            pass
        else:
            messages.add_message(request, messages.INFO, 'You need to login in to make a post.')
            return redirect("login")
        f = PostForm(request.POST)
        if f.is_valid():
            object = f.save(commit=False)
            object.section = community
            object.user = request.user
            object.save()
            messages.add_message(request, messages.SUCCESS, 'New comment created')

    else:
        f = PostForm()



    return render(request, 'app/secpage.html', {'form': f, 'posts': g, 'section': community})

class MainListView(ListView):
    model = Post
    template_name = 'app/mainpage.html'
    context_object_name = 'posts'

    def get_queryset(self):
        return Post.objects.all().order_by('-created_on')

class SectionListView(ListView):
    model = Post
    template_name = 'app/secpage.html'
    context_object_name = 'posts'

    def get_queryset(self):
        return Post.objects.all().order_by('-created_on')

class PopularListView(MainListView):
    def get_queryset(self):
        return Post.objects.all().order_by('-likes')


def post(request, pk):
    object = get_object_or_404(Post, id=pk)
    g = object.comment_set.all().order_by('-created_on')
    if request.method == 'POST':
        f = CommentForm(request.POST)
        if f.is_valid():
            if request.user.is_authenticated:
                pass
            else:
                messages.add_message(request, messages.INFO, 'You need to login in to make a post.')
                return redirect("login")
            box = f.save(commit=False)
            box.post = object
            box.user = request.user
            f.save()
            messages.add_message(request, messages.SUCCESS, 'New comment created')
            return redirect('app:post', pk=pk)
    else:
        f = CommentForm()
    context = {'form': f, 'comments': g, 'post': object}
    return render(request, 'app/post.html', context)

def search(request):
    f = SearchForm(request.GET)
    post_list = []

    if f.is_valid():

        query = f.cleaned_data.get('query')
        if query:
            post_title = Post.objects.filter(title__icontains=query)
            post_text = Post.objects.filter(text__icontains=query)
            post_list = (post_title | post_text).distinct()

        return render(request, 'app/search.html', {'posts': post_list, 'query': query})


#    return render(request, 'app/core.html', {'search': f})

#def comment(request, post_id, head_comment):
#    post = get_object_or_404(Post, pk=post_id)
#    if request.method == 'POST':
#        f = CommentForm(request.POST)
#        if f.is_valid():
#            g = Comment.objects.get(pk=head_comment)
#            f.replying_to = g
#            f.post = post
#            f.user = request.user
#            f.save()
#            messages.add_message(request, messages.SUCCESS, 'Comment sent')
#            return redirect('')
#    else:
 #       f = CommentForm()
#
#    return render(request, 'app/postpage.html', {'form':f})

@login_required()
def response(request, pk):
    post = Post.objects.get(id=pk)
    if request.POST:
        f = CommentForm(request.POST)
        if f.is_valid():
            object = f.save(commit=False)
            object.user = request.user
            object.post = post
            f.save()
            messages.success(request, 'Your comment was successfully created.')
            return redirect('app:post', pk=pk)
    else:
        f = CommentForm()

    return render(request, 'app/commentpage.html', {'form': f})


@login_required
def update_comment(request, pk):
    k = Comment.objects.get(id=pk)
    post_id = k.post.id
    if request.POST:
        f = CommentForm(request.POST, instance=k)
        if f.is_valid():
            f.save()
            messages.success(request, 'Your comment has been updated.')
            return redirect('app:post', pk=post_id)
    else:
        f = CommentForm(instance=k)

    return render(request, 'app/commentcore.html', {'form':f, 'pk': pk})

@login_required
def delete_comment(request, pk):
    k = Comment.objects.get(id=pk)
    post_id = k.post.id
    k.delete()
    messages.success(request, 'Your comment has been deleted.')
    return redirect('app:post', pk=post_id)

@login_required
def update_post(request, pk):
    k = Post.objects.get(id=pk)
    if request.POST:
        f = PostForm(request.POST, instance=k)
        if f.is_valid():
            f.save()
            pk = k.section.id
            messages.success(request, 'Your post has been updated.')
            return redirect('app:section', pk=pk)
    else:
        f = PostForm(instance=k)

    return render(request, 'app/replycore.html', {'form': f, 'post_id': pk})

@login_required
def delete_post(request, pk):
    post = Post.objects.get(id=pk)
    g = post.section.id
    post.delete()
    messages.success(request, 'Your post has been deleted.')
    return redirect('app:section', pk=g)


def cancel(request):
    next_url = request.GET.get('next')
    if next_url:
        return HttpResponseRedirect(next_url)
    else:
       return redirect('app:index')


def signup(request):
    if request.user.is_authenticated:
        messages.success(request, "You're already logged in.")
        return redirect('app:index')

    if request.method == 'POST':
        f = CreateUserForm(request.POST)
        if f.is_valid():
            f.save()
            messages.success(request, 'Account created successfully. You can now log in.')
            return redirect('login')
    else:
        f = CreateUserForm()
    return render(request, 'app/signin.html', {'form': f})


def login(request):
    if request.user.is_authenticated:
        return redirect('app:index')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')


        user = auth.authenticate(username=username, password=password)

        if user is not None:
            # correct username and password login the user
            auth.login(request, user)
            return redirect('app:index')

        else:
            messages.error(request, 'Error wrong username/password')

    return render(request, 'app/reallogin.html')

@login_required
def logout(request):
    auth.logout(request)
    return render(request, 'app/outpage.html')



