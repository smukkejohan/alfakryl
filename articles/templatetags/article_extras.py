# -*- coding: utf-8 -*-

from django import template
from articles.models import Article

register = template.Library()

def get_latest_articles(parser, token):
    bits = token.contents.split()
    if len(bits) != 2:
        raise TemplateSyntaxError, "get_latest_articles tag takes exactly one argument"
    return LatestArticlesNode(bits[1])

class LatestArticlesNode(Node):
    def __init__(self, num):
        self.num = num
    
    def render(self, context):
        context['latest_articles'] = Article.get_published()[:self.num]
        return ''

def render_month_links(template.Node):
    return {
        'dates': Article.objects.dates('pub_date', 'month'),
    }
register.inclusion_tag('articles/month_links_snippet.html')(render_month_links)
