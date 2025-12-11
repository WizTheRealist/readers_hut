from django import template
from django.db.models import Count
from blog.models import Post
from taggit.models import Tag

register = template.Library()

@register.simple_tag
def get_recent_posts(count=5):
    return Post.objects.filter(status='published').order_by('-published_date')[:count]

@register.simple_tag
def get_popular_posts(count=5):
    return Post.objects.filter(status='published').order_by('-views')[:count]

@register.simple_tag
def get_popular_tags(count=10):
    return Tag.objects.annotate(
        num_times=Count('taggit_taggeditem_items')
    ).order_by('-num_times')[:count]

@register.filter
def reading_time(content):
    # Estimate reading time based on word count
    # Average reading speed: 200 words per minute
    import re
    from django.utils.html import strip_tags
    
    text = strip_tags(content)
    word_count = len(re.findall(r'\w+', text))
    minutes = word_count / 200
    return int(minutes) if minutes > 1 else 1