from django import template
from blog.models import Post

register = template.Library()


@register.inclusion_tag('popular_post_tpl.html')
def get_popular_post(cnt=5):
    post_pop = Post.objects.order_by('-views')[:cnt]
    print({'posts': post_pop})
    return {'posts': post_pop}
