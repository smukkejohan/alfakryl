# -*- coding: utf-8 -*-

from django import template
from articles.models import Article, Section

register = template.Library()

def render_article(obj, h_tag = 'h2'):
    return {
        'object': obj,
        'h_tag': h_tag
    }
register.inclusion_tag('articles/list_snippet.html')(render_article)
    
def get_crud_links(context, article):
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

def section_links(num):
    return {
        'sections': Section.objects.all()[:num],
    }
register.inclusion_tag('articles/section_links_snippet.html')(section_links)

#def get_crud_links(parser, token):
#    try:
#        tag_name, article, user = token.split_contents()
#    except ValueError:
#        raise template.TemplateSyntaxError, "%r tag requires exactly two arguments" % token.contents.split()[0]
#    return CrudLinksNode(article, user)

#register.tag(get_crud_links)

#class CrudLinksNode(template.Node):
#    def __init__(self, article, user):
#        self.article = template.Variable(article)
#        self.user = template.Variable(user)
#    
#    def render(self, context):
#        try:
#            user = self.user.resolve(context)
#            article = self.article.resolve(context)
#            if article.authors.all().get(pk=user.id):
#                context['crud_links'] = True
#                return ''      
#        except template.VariableDoesNotExist:
#            return ''
#        return ''
    
# most read
#def get_latest_articles(parser, token):
#    bits = token.contents.split()
#    if len(bits) != 2:
#        raise TemplateSyntaxError, "get_latest_articles tag takes exactly one argument"
#    return LatestArticlesNode(bits[1])
#
#class LatestArticlesNode(Node):
#    def __init__(self, num):
#        self.num = num
#    
#    def render(self, context):
#        context['latest_articles'] = Article.get_published()[:self.num]
#        return ''
#
#def render_month_links(template.Node):
#    return {
#        'dates': Article.objects.dates('pub_date', 'month'),
#    }
#register.inclusion_tag('articles/month_links_snippet.html')(render_month_links)
