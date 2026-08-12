from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import ifestImage, Partners_Supporters, GalleryImage, Gifts, LatestNews




@admin.register(Partners_Supporters)
class PartnersSupportersAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'order')
    list_filter = ('category',)
    ordering = ('order',)


@admin.register(GalleryImage)
class GalleryImageAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'category', 'uploaded_at')
    list_filter = ('category',)


@admin.register(Gifts)
class GiftsAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'order')
    ordering = ('order',)


@admin.register(LatestNews)
class LatestNewsAdmin(SummernoteModelAdmin):
    summernote_fields = ('description', 'body')
    list_display = ('title', 'date')
    search_fields = ('title',)
    ordering = ('-date',)
