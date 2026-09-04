from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.db.models import Q
from django.core.paginator import Paginator

from .models import App, Category

SORTS = {
    'new': '-created_at',
    'name': 'name',
    'price': 'price',
    'expensive': '-price',
}


def index(request):
    q = request.GET.get('q', '')
    sort = request.GET.get('sort', 'new')

    if q:
        apps = App.objects.filter(Q(name__icontains=q) | Q(description__icontains=q))
    else:
        apps = App.objects.all()

    apps = apps.order_by(SORTS.get(sort, '-created_at'))
    featured = App.objects.order_by('-price').first()
    categories = Category.objects.all()

    paginator = Paginator(apps, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'main/index.html', {
        'q': q,
        'sort': sort,
        'page_obj': page_obj,
        'featured': featured,
        'categories': categories,
    })


def about(request):
    return render(request, 'main/about.html')


def app_detail(request, app_id):
    app = get_object_or_404(App, id=app_id)
    return render(request, 'main/app_detail.html', {'app': app})


def category_detail(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    apps = App.objects.filter(category=category)
    return render(request, 'main/category.html', {
        'category': category,
        'apps': apps,
    })


def new(request):
    apps = App.objects.order_by('-created_at')[:5]
    return render(request, 'main/new.html', {'apps': apps})
