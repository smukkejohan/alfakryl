# -*- coding: utf-8 -*-

from django.contrib.syndication.feeds import Feed
from articles.models import Article
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.syndication.feeds import FeedDoesNotExist

class LatestArticles(Feed):
    title = "Alfakryl"
    link = "/"
    description = "Seneste artikler på alfakryl.dk"

    def items(self):
        return Article.objects.published().order_by('-pub_date')[:12]
    
    def item_pubdate(self, item):
        return item.pub_date

class LatestArticlesBySection(Feed):
    def get_object(self, bits):
        if len(bits) != 1:
            raise ObjectDoesNotExist
        return Section.objects.get(title__exact=bits[0])
    
    def title(self, obj):
        return "Alfakryl.dk: sektionen %s" % obj.title
    
    def link(self, obj):
        if not obj:
            raise FeedDoesNotExist
        return obj.get_absolute_url()

    def description(self, obj):
        return "Seneste artikler i sektionen %s" % obj.title
            
    def items(self):
        return Article.objects.published().filter(sections=obj).order_by('-pub_date')[:12]


