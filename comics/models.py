from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.files.base import ContentFile
from zipfile import ZipFile
import os
from django.core.files.storage import default_storage
from django.utils.timesince import timesince


class User(AbstractUser):
    bio = models.CharField(max_length=250, default='')
    pass


class Series(models.Model):
    cover = models.ImageField(upload_to="media")
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               max_length=140, related_name='series')
    title = models.CharField(unique=True, max_length=40)
    finished = models.BooleanField(default=False)
    fav = models.ManyToManyField(User,
                                 blank=True, related_name='favs')
    about = models.TextField(max_length=1000, default="")

    def serialize(self):
        return {
            'cover': self.cover.url,
            'author': self.author.username,
            'title': self.title,
            'favs': self.fav.count()
        }


class Chapter(models.Model):
    series = models.ForeignKey(Series, on_delete=models.CASCADE,
                               max_length=40, related_name='chapters')
    chap = models.IntegerField()
    zip_import = models.FileField(upload_to="media")
    views = models.IntegerField(default=0)
    timestamp = models.DateTimeField(auto_now_add=True)

    def serialize(self):
        return {
            'cover': self.series.cover.url,
            'author': self.series.author.username,
            'title': self.series.title,
            'chap': self.chap,
            'timestamp': timesince(self.timestamp).replace('\xa0', ' ')+' ago',
            'favs': self.series.fav.count(),
            'views': self.views
        }

    class Meta:
        constraints = [models.UniqueConstraint(
            fields=('series', 'chap'), name='unique_chapter')]

    def is_valid(self):
        try:
            zip_file = ZipFile(self.zip_import)
        except:
            return False
        names = []
        for name in zip_file.namelist():
            if not name.startswith('__MACOSX/') and not name.endswith("/"):
                names.append(name)
        zip_file.close()
        if len(names) == 0:
            return False
        else:
            for name in names:
                (base, ext) = os.path.splitext(name)
                if ext not in ('.png', '.jpg'):
                    return False
                try:
                    int(os.path.basename(base))
                except:
                    return False
            return True

    def delete_import(self):
        self.zip_import.delete(save=True)

    def to_gallery(self):
        zip_file = ZipFile(self.zip_import)
        for name in zip_file.namelist():
            if not name.startswith('__MACOSX/'):
                data = zip_file.read(name)
                name = os.path.split(name)[1]
                path = os.path.join(
                    "media", name
                )
                saved_path = default_storage.save(path, ContentFile(data))

                img = GalleryImage(series=self.series,
                                   chap=self.chap, file=saved_path)
                img.save()
        zip_file.close()
        self.zip_import.delete(save=True)


class GalleryImage(models.Model):
    series = models.ForeignKey(Series, on_delete=models.CASCADE,
                               max_length=40, related_name='chapters_images')
    chap = models.IntegerField()
    file = models.ImageField(upload_to="media")
