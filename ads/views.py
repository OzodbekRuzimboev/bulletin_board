from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (ListView, DetailView, CreateView, UpdateView, DeleteView)
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Ad, Category, AdImage, AdVideo, AdFile
from .forms import AdForm, AdSearchForm
import logging
from django.urls import reverse_lazy
from ads.services.media import MediaService
import re

logger = logging.getLogger(__name__)

class HomeView(ListView):
    model = Ad
    template_name = 'ads/home.html'
    context_object_name = 'ads'
    ordering = ['-date_posted']
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_form'] = AdSearchForm()
        return context

class AdCreateView(LoginRequiredMixin, CreateView):
    model = Ad
    form_class = AdForm
    template_name = 'ads/ad_form.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        form.instance.author = self.request.user
        response = super().form_valid(form)
        MediaService.attach(self.object, self.request.FILES)
        messages.success(self.request, 'Ваше объявление создано!')
        return response
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Создать объявление'
        return context

class AdDetailView(DetailView):
    model = Ad
    template_name = 'ads/ad_detail.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class AdUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Ad
    form_class = AdForm
    template_name = 'ads/ad_update_form.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Обновить объявление'
        context['ad_images'] = self.object.images.all()
        context['ad_videos'] = self.object.videos.all()
        context['ad_files'] = self.object.files.all()
        return context
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()

        self._process_deletions(request)
        response = self.form_valid(form)
        MediaService.attach(self.object, request.FILES)
        messages.success(request, 'Ваше объявление обновлено!')
        return response
    
    def _process_deletions(self, request):
        map_ = (
            (AdImage, 'images_to_delete'),
            (AdVideo, 'videos_to_delete'),
            (AdFile,  'files_to_delete'),
        )
        for model, field in map_:
            ids = [int(pk) for pk in request.POST.get(field, '').split(',') if pk]
            for obj in model.objects.filter(id__in=ids, ad=self.object):
                MediaService.delete(obj)

    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
    def test_func(self):
        ad = self.get_object()
        return self.request.user == ad.author

class AdDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Ad
    template_name = 'ads/ad_confirm_delete.html'
    success_url = '/'
    
    def test_func(self):
        ad = self.get_object()
        return self.request.user == ad.author
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class UserAdListView(ListView):
    model = Ad
    template_name = 'ads/user_ads.html'
    context_object_name = 'ads'
    
    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Ad.objects.filter(author=user).order_by('-date_posted')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['username'] = self.kwargs.get('username')
        return context

class CategoryAdListView(ListView):
    model = Ad
    template_name = 'ads/category_ads.html'
    context_object_name = 'ads'
    
    def get_queryset(self):
        category = get_object_or_404(Category, name=self.kwargs.get('category'))
        return Ad.objects.filter(category=category).order_by('-date_posted')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = get_object_or_404(Category, name=self.kwargs.get('category'))
        return context

# ────────────────────────────────────────────────
def _build_text_query(words):
    q = Q()
    for w in words:
        part = Q(title__icontains=w) | Q(description__icontains=w)
        q &= part
    return q

# ────────────────────────────────────────────────
def search_ads(request):
    form = AdSearchForm(request.GET)
    ads = Ad.objects.all()

    if form.is_valid():
        data  = form.cleaned_data
        raw   = (data.get("query") or "").strip()
        words = re.split(r"\s+", raw.lower()) if raw else []

        # ---------- основной поиск ----------
        if words:
            ads = ads.filter(_build_text_query(words))

            # ---------- fallback по ключам ----------
            if not ads.exists():
                cats = Category.objects.filter(
                    keywords__iregex=rf"(^|,\s*){re.escape(raw.lower())}(\s*,|$)"
                )
                ads = Ad.objects.filter(category__in=cats)

        # ---------- остальные фильтры ----------
        if data["category"]:
            ads = ads.filter(category=data["category"])
        if data["min_price"]:
            ads = ads.filter(price__gte=data["min_price"])
        if data["max_price"]:
            ads = ads.filter(price__lte=data["max_price"])
        if data["location"]:
            ads = ads.filter(location__icontains=data["location"])

    return render(
        request,
        "ads/search_results.html",
        {"ads": ads.order_by("-date_posted"), "form": form},
    )