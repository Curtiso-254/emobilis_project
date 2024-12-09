from django.shortcuts import redirect, render
from .models import Post
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required

def post_list(request):
    posts = Post.objects.all().order_by('-pub_date')
    paginator = Paginator(posts, 5)  # Show 5 posts per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'blog/post_list.html', {'page_obj': page_obj})

from django.contrib.auth.decorators import login_required

@login_required
def create_post(request):
      if request.method == 'POST':
           title = request.POST.get('title')
           content = request.POST.get('content')
           post = Post(title=title, content=content, author=request.user) 
           post.save()
           return redirect('post_list')
      return render(request, 'blog/create_post.html')