from django.contrib import admin
from .models import *

# This is a extra. Only users should upload chapters.
# If something unexpected arises, the admin have the option to upload a chapter (.zip file).
# If .zip file is valid, an action is implemented so it can be rendered as a readable chapter (GalleryImage instance).
# A second action is implemented so the admin can delete a Series instance and its related files. 

@admin.action(description='Extract images from zip files.')
def from_chapter_to_gallery(modeladmin, request, queryset):
# creating a GalleryImage object from a Chapter object.
    for q in queryset:
        if q.zip_import.name!='':
            if q.is_valid():
                q.to_gallery()
            else:
                q.delete_import()
                q.delete()
                
@admin.action(description='Delete a series')
def delete_series(modeladmin, request, queryset):
    for q in queryset:
        pages=q.chapter_images.all()
        for page in pages:
            page.file.delete(save=True)
            page.delete()
        q.chapters.all().delete()

class uploader(admin.ModelAdmin):
    actions = [from_chapter_to_gallery]
class deleter(admin.ModelAdmin):
    actions = [delete_series]
    
admin.site.register(User)
admin.site.register(Series,deleter)
admin.site.register(Chapter,uploader)
admin.site.register(GalleryImage)