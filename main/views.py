from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.db.models import Q
from django.core.paginator import Paginator
from django.views.decorators.http import require_GET

from django.views.generic import TemplateView, ListView, DetailView

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


# @require_GET
# def about(request):
#     return render(request, 'main/about.html')


class AboutView(TemplateView):
    template_name = 'main/about.html'


# def app_detail(request, app_id):
#     app = get_object_or_404(App, id=app_id)
#     return render(request, 'main/app_detail.html', {'app': app})


class AppDetailView(DetailView):
    model = App
    template_name = 'main/app_detail.html'
    context_object_name = 'app'
    pk_url_kwarg = 'app_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        app = self.object
        context['similar_apps'] = (
            App.objects.filter(
                price__gte=app.price - 10,
                price__lte=app.price + 10,
            )
            .exclude(id=app.id)[:3]
        )
        return context


def category_detail(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    apps = App.objects.filter(category=category)
    return render(request, 'main/category.html', {
        'category': category,
        'apps': apps,
    })


# def new(request):
#     apps = App.objects.order_by('-created_at')[:5]
#     return render(request, 'main/new.html', {'apps': apps})


class NewAppView(ListView):
    model = App
    template_name = 'main/new.html'
    context_object_name = 'apps'
    ordering = ['-created_at']
    paginate_by = 3


# def apps_list(request, is_free):
#     if is_free:
#         apps = App.objects.filter(price=0)
#         title = 'Бесплатные приложения'
#     else:
#         apps = App.objects.filter(price__gt=0)
#         title = 'Платные приложения'
#
#     return render(request, 'main/apps_list.html', {
#         'apps': apps,
#         'title': title,
#     })


class AppsIsFreeListView(ListView):
    model = App
    template_name = 'main/apps_list.html'
    context_object_name = 'apps'

    def get_queryset(self):
        if self.kwargs.get('is_free'):
            return App.objects.filter(price=0)
        return App.objects.filter(price__gt=0)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.kwargs.get('is_free'):
            context['title'] = 'Бесплатные приложения'
        else:
            context['title'] = 'Платные приложения'
        return context


def api_app_detail(request, app_id):
    app = get_object_or_404(App, id=app_id)
    data = {
        'id': app.id,
        'name': app.name,
        'description': app.description,
        'price': app.price,
    }
    return JsonResponse(data)
