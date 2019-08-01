from django import template
from cms_app.models import Post

register = template.Library()

@register.simple_tag
def num_posts():
    count = Post.objects.all().count()
    return count

@register.inclusion_tag('cms_app/index.html')
def ps():
    posts = Post.objects.all()
    return {'psc':posts}

@register.simple_tag
def float_to_int(number):
    return int(number)
