from django import forms
from .models import Ad, AdImage, AdVideo, AdFile, Category

class AdForm(forms.ModelForm):
    class Meta:
        model = Ad
        fields = ['title', 'description', 'price', 'category', 'location', 'contact_info']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 5}),
        }
        labels = {
            'title': 'Название',
            'description': 'Описание',
            'price': 'Цена',
            'category': 'Категория',
            'location': 'Местоположение',
            'contact_info': 'Контактная информация'
        }

class AdImageForm(forms.Form):
    images = forms.FileField(
        label='Изображения',
        required=False
    )

class AdVideoForm(forms.ModelForm):
    video = forms.FileField(required=False, label='Видео')
    
    class Meta:
        model = AdVideo
        fields = ['video']

class AdFileForm(forms.ModelForm):
    file = forms.FileField(required=False, label='Файл')
    
    class Meta:
        model = AdFile
        fields = ['file']

class AdSearchForm(forms.Form):
    query = forms.CharField(required=False, label='Поиск', widget=forms.TextInput(attrs={'placeholder': 'Поиск...'}))
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        required=False, 
        empty_label="Все категории",
        label='Категория'
    )
    min_price = forms.DecimalField(required=False, min_value=0, label='Мин. цена')
    max_price = forms.DecimalField(required=False, min_value=0, label='Макс. цена')
    location  = forms.CharField(required=False, label='Местоположение')
