from django.contrib.sitemaps import Sitemap

from .models import Women, Category


class PostSitemap(Sitemap):  # https://docs.djangoproject.com/en/4.2/ref/contrib/sitemaps/#sitemap-class-reference
    changefreq = 'monthly'
    priority = 0.9

    def items(self):  # возвращает записи из карты сайта
        return Women.published.all()

    def lastmod(self, obj):  # возвращает время последнего изменения страницы
        return obj.time_update


class CategorySitemap(Sitemap):  # https://docs.djangoproject.com/en/4.2/ref/contrib/sitemaps/#sitemap-class-reference
    changefreq = 'monthly'  # частота
    priority = 0.9  # приоритет

    def items(self):  # возвращает записи из карты сайта
        return Category.objects.all()


