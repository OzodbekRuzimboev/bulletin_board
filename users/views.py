from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from ads.models import Category
import os

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Аккаунт создан для пользователя {username}! Теперь вы можете войти.')
            return redirect('login')
    else:
        form = UserRegisterForm()
    
    context = {
        'form': form,
        'categories': Category.objects.all()
    }
    return render(request, 'users/register.html', context)

@login_required
def profile(request):
    if request.method == 'POST':

        # Удаление фотографии профиля
        if 'delete_photo' in request.POST:
            profile = request.user.profile

            if profile.image and profile.image.name != 'default_profile.png':
            
                if os.path.isfile(profile.image.path):
                    os.remove(profile.image.path)
                
                profile.image = 'default_profile.png'
                profile.save()
                messages.success(request, 'Фото профиля удалено.')
                
            else:
                messages.info(request, 'Вы уже используете фото профиля по умолчанию.')

            return redirect('profile')
        
        # Обновление фотографии профиля
        elif 'update_photo' in request.POST:

            if 'image' in request.FILES:
                profile = request.user.profile

                if profile.image and profile.image.name != 'default_profile.png':

                    if os.path.isfile(profile.image.path):
                        os.remove(profile.image.path)

                profile.image = request.FILES['image']
                profile.save()
                messages.success(request, 'Фото профиля обновлено.')

                return redirect('profile')
        
        # Обновление профиля
        else:
            u_form = UserUpdateForm(request.POST, instance=request.user)
            p_form = ProfileUpdateForm(request.POST, instance=request.user.profile)
            
            if u_form.is_valid() and p_form.is_valid():
                u_form.save()
                p_form.save()
                messages.success(request, 'Ваш профиль обновлен!')
                return redirect('profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
    
    context = {
        'u_form': u_form,
        'p_form': p_form,
        'categories': Category.objects.all()
    }
    
    return render(request, 'users/profile.html', context)