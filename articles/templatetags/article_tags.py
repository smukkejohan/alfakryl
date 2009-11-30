# -*- coding: utf-8 -*-

from django import template
from articles.models import Article, Section

register = template.Library()
    
def get_crud_links(context, article):
    if context['user'].is_superuser:
        crud_perms = True
    else:
        try:
            article.authors.all().get(pk=context['user'].id)
            crud_perms = True
        except:
            crud_perms = False
    
    return { 
        'article': article,
        'crud_perms': crud_perms
    } 
register.inclusion_tag('articles/red/crud_links.html', takes_context=True)(get_crud_links)

def month_links(num):
    return {
        'dates': Article.objects.published().dates('pub_date', 'month')[:num],
    }
register.inclusion_tag('articles/month_links_snippet.html')(month_links)

@register.tag()
def get_sections(parser, token):
    try:
        # split_contents() knows not to split quoted strings.
        tag_name, max_num = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError, "%r tag requires exactly one arguments" % token.contents.split()[0]
    return SectionsNode(max_num)
 
class SectionsNode(template.Node):
    def __init__(self, max_num):
        self.max_num = max_num
    def render(self, context):
        context['sections'] = Section.objects.all().filter(importance__gte=1)[:self.max_num]
        return ''



