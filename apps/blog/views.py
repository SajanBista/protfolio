from django.shortcuts import get_object_or_404, render

from .models import BlogPost, Tag


def post_list(request):
    posts = BlogPost.objects.filter(status=BlogPost.Status.PUBLISHED)

    tag_slug = request.GET.get("tag")
    active_tag = None
    if tag_slug:
        active_tag = get_object_or_404(Tag, slug=tag_slug)
        posts = posts.filter(tags=active_tag)

    context = {
        "posts": posts,
        "tags": Tag.objects.all(),
        "active_tag": active_tag,
    }
    return render(request, "blog/post_list.html", context)


def post_detail(request, slug):
    post = get_object_or_404(BlogPost, slug=slug, status=BlogPost.Status.PUBLISHED)
    return render(request, "blog/post_detail.html", {"post": post})
