from django.db import transaction
from ads.models import AdImage, AdVideo, AdFile

class MediaService:
    @staticmethod
    @transaction.atomic
    def attach(ad, files):
        for img in files.getlist('images'):
            AdImage.objects.create(ad=ad, image=img)
        if video := files.get('video'):
            AdVideo.objects.create(ad=ad, video=video)
        if file_obj := files.get('file'):
            AdFile.objects.create(ad=ad, file=file_obj, file_name=file_obj.name)

    @staticmethod
    def delete(instance):
        """
        Удаляет и физический файл, и запись в БД.
        Подходит для AdImage, AdVideo, AdFile.
        """
        f = getattr(instance, 'image', None) or getattr(instance, 'file', None) or getattr(instance, 'video', None)
        if f:
            f.delete(save=False)
        instance.delete()
