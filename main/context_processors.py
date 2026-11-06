from django.db.models import Count
from django.core.cache import cache

from .models import App, Category


def store_menu(request):
    categories = cache.get('menu_categories')
    if categories is None:
        categories = list(
            Category.objects
            .annotate(apps_count=Count('app'))
            .order_by('name')
        )
        cache.set('menu_categories', categories, 60 * 3)
    favorites_count = 0
    if request.user.is_authenticated:
        favorites_count = request.user.favorite_apps.count()

    apps_total = cache.get('cache_apps_total')
    if apps_total is None:
        apps_total = App.objects.count()
        cache.set('cache_apps_total', apps_total, 60 * 10)

    categories_total = cache.get('cache_categories_total')
    if categories_total is None:
        categories_total = len(categories)
        cache.set('cache_categories_total', categories_total, 60 * 10)

    return {
        'categories': categories,
        'apps_total': apps_total,
        'categories_total': categories_total,
        'favorites_count': favorites_count,
    }
