from django.contrib import admin
from .models import Category, Ad, AdImage, AdVideo, AdFile

class AdImageInline(admin.TabularInline):
    model = AdImage
    extra = 1

class AdVideoInline(admin.TabularInline):
    model = AdVideo
    extra = 1

class AdFileInline(admin.TabularInline):
    model = AdFile
    extra = 1

class AdAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'author', 'price', 'date_posted')
    list_filter = ('category', 'date_posted')
    search_fields = ('title', 'description', 'author__username')
    inlines = [AdImageInline, AdVideoInline, AdFileInline]

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'keywords')
    search_fields = ('name', 'keywords', 'description')

admin.site.register(Category, CategoryAdmin)
admin.site.register(Ad, AdAdmin)
