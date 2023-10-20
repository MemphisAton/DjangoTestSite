from django import template
from django.db.models import Count, Q

import women.views as views

from women.models import Category, TagPost

register = template.Library()


@register.inclusion_tag('women/list_categories.html')
def show_categories(cat_selected=0):
    #cats = Category.objects.annotate(total=Count('posts')).filter(total__gt=0)
    cats = Category.objects.annotate(total_posts=Count('posts', filter=Q(posts__is_published=True))).filter(
        total_posts__gt=0)

    return {'cats': cats, 'cat_selected': cat_selected}


@register.inclusion_tag('women/list_tags.html')
def show_all_tags(cat_selected=0):
    return {'tags': TagPost.objects.annotate(total=Count('tags')).filter(total__gt=0)}