from django.db import models
from django.conf import settings
from django.urls import reverse
from django.utils import timezone

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    keywords = models.CharField(max_length=255, blank=True, help_text="Ключевые слова для этой категории, разделенные запятыми")
    position = models.IntegerField(default=0, help_text="Контролирует порядок отображения категорий")
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = 'Категории'
        verbose_name = 'Категория'
        ordering = ['position', 'name']
        

class Ad(models.Model):
    title = models.CharField(max_length=200, verbose_name='Название')
    description = models.TextField(blank=True, verbose_name='Описание')
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name='Цена')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='ads', verbose_name='Категория')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='ads', verbose_name='Автор')
    location = models.CharField(max_length=100, blank=True, verbose_name='Местоположение')
    contact_info = models.CharField(max_length=100, verbose_name='Контактная информация')
    date_posted = models.DateTimeField(default=timezone.now, verbose_name='Дата публикации')
    
    def __str__(self): # отвечает за строковое представление объекта модели
        return self.title
    
    # служебный класс Django, который позволяет задавать метаданные модели
    class Meta:
        verbose_name = 'Объявление'
        verbose_name_plural = 'Объявления'
        ordering = ['-date_posted']
    

    # метод, который возвращает URL, по которому можно посмотреть детальную страницу объекта
    def get_absolute_url(self):
        return reverse('ad-detail', kwargs={'pk': self.pk})

class AdImage(models.Model):
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='ad_images', verbose_name='Изображение')
    
    class Meta:
        verbose_name = 'Изображение'
        verbose_name_plural = 'Изображения'
    
    def __str__(self):
        return f"Изображение для {self.ad.title}"

class AdVideo(models.Model):
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE, related_name='videos')
    video = models.FileField(upload_to='ad_videos', verbose_name='Видео')
    
    class Meta:
        verbose_name = 'Видео'
        verbose_name_plural = 'Видео'
    
    def __str__(self):
        return f"Видео для {self.ad.title}"

class AdFile(models.Model):
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE, related_name='files')
    file = models.FileField(upload_to='ad_files', verbose_name='Файл')
    
    class Meta:
        verbose_name = 'Файл'
        verbose_name_plural = 'Файлы'
    
    def __str__(self):
        return self.file.name