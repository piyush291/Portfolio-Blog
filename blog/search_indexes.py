import datetime
from haystack import indexes
from blog.models import post

class BlogIndex(indexes.SearchIndex, indexes.indexable):
    pass