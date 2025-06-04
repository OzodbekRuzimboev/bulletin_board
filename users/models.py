from django.db import models
from django.contrib.auth.models import User
from PIL import Image
import os

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default_profile.png', upload_to='profile_pics', verbose_name='Изображение профиля')
    phone = models.CharField(max_length=15, blank=True, verbose_name='Телефон')
    
    def __str__(self):
        return f'Профиль пользователя {self.user.username}'
    
    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        
        if self.image and os.path.isfile(self.image.path):
            img = Image.open(self.image.path)
            if img.height > 300 or img.width > 300:
                output_size = (300, 300)
                img.thumbnail(output_size)
                img.save(self.image.path)
