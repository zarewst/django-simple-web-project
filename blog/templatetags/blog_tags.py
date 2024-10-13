from django import template
from blog.models import Category, Article


register = template.Library()


@register.simple_tag()
def get_categories():
    return Category.objects.all()


# @register.simple_tag()
# def get_article_photo(pk):
#     article = Article.objects.get(pk=pk)
#     if 'https' in article.photo:
#         return article.photo
#
#     else:
#         return article.photo.url

