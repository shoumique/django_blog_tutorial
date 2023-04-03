from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Post
from .forms import PostForm

# Create your views here.
def post_list(request):

    if request.method == 'POST':
        # if request.POST.get('action') == 'unpublish':
        #     print("Unpublished clicked")
        #     print(request.POST)
        # if request.POST.get('action') == 'delete':
        #     print("DELETE clicked")
        for key, value in request.POST.items():
            if value.endswith('_unpublish'):
                pk = value.split('_')[0]
                action = 'unpublish'
            elif value.endswith('_delete'):
                pk = value.split('_')[0]
                action = 'delete'
            else:
                pk = None
                action = None
            
            if pk is not None and action is not None:
                pk = int(pk)
                post = Post.objects.get(pk=pk)

                if post:
                    if action == 'unpublish':
                        post.unpublish()
                    elif action == 'delete':
                        post.delete()
                else:
                    # There is no Post object with the specified primary key
                    raise Http404("Post does not exist")

    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')

    return render(request, 'blog/post_list.html', {'posts': posts})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)

    return render(request, 'blog/post_detail.html', {'post': post})

@login_required
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)

        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            # post.published_date = timezone.now()
            post.save()

            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()

    return render(request, 'blog/post_edit.html', {'form': form})

@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if request.method == "POST":
        form = PostForm(request.POST, instance=post)

        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            # post.published_date = timezone.now()
            post.save()

            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)

    return render(request, 'blog/post_edit.html', {'form': form})

def post_draft_list(request):
    posts = Post.objects.filter(published_date__isnull=True).order_by('created_date')
    return render(request,'blog/post_draft_list.html', {'posts': posts})

def publish_post(request,pk):
    post = get_object_or_404(Post, pk=pk)

    if post:
        post.publish()

    return redirect('post_detail', pk=post.pk)


def unpublish_post(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if post:
        post.unpublish()

    return redirect('post_detail', pk=post.pk)

def delete_post(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if post:
        post.delete()

    return redirect('post_list')
