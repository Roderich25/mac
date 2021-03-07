from django.views.generic import ListView
from blog.models import Post


class BlogView(ListView):
    model = Post
    context_object_name = 'posts'
    template_name = 'blog/blog.html'
