import markdown
from django import template
from django.db.models import Count
from django.utils.safestring import mark_safe

from ..models import Post

register = template.Library()


@register.simple_tag
def total_posts():
    """Общее число опубликованных в блоге постов"""
    return Post.published.count()


@register.inclusion_tag("blog/post/latest_posts.html")
def show_latest_posts(count=5):
    """Последние опубликованные посты"""
    latest_posts = Post.published.order_by("-publish")[:count]
    return {"latest_posts": latest_posts}


@register.simple_tag
def get_most_commented_posts(count=0):
    """Самые закоментированные посты"""
    total_comments_by_post = Post.published.annotate(
        total_comments=Count("comments")
    ).order_by("-total_comments")[:5]
    for i in range(len(total_comments_by_post)):
        if total_comments_by_post[i].total_comments > 0:
            count += 1
    return Post.published.annotate(total_comments=Count("comments")).order_by(
        "-total_comments"
    )[:count]


@register.filter(name="markdown")
def markdown_format(text):
    return mark_safe(markdown.markdown(text))
