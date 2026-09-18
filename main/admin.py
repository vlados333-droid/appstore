from django.contrib import admin
from .models import Category, App, Review


admin.site.register(Category)


@admin.register(App)
class AppAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'category', 'created_at')
    search_fields = ('name', 'description')
    list_filter = ('category',)


admin.site.register(Review)
