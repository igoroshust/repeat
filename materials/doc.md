- Миграции - файлы для настройки базы данных, которые указывают базе, как и какая информация будет в ней хранится.
- asgiref Поддержка асинхронности (ASGI)
- pkg-resources	- Управление метаданными пакетов (часть setuptools)
- pytz - Работа с часовыми поясами
- setuptools - Сборка и установка пакетов
- sqlparse - Анализ и форматирование SQL‑запросов


- csrf token - CSRF (Cross-Site Request Forgery) — атака, когда злоумышленник заставляет авторизованного пользователя выполнить нежелательное действие.

- Дженерики

- SQLAlchemy

- Оптимизация ORM-запросов в Django

- Celery + разница shared_task и shedules






















# Контекст
context - python-словарь `{'key': value}`, который Django передаёт в шаблон для рендера
```python
context = {
    'object_list': <QuerySet>,
    'page_obj': <Page>,
    'categories': <QuerySet>,
}
return render(request, 'template.html', context)
```

# Дженерики
Дженерики - готовый классы-представления для типичных задач (CRUD), избавляющие от написания boilerplate-кода. 

**Основные группы**
- ListView
- DetailView
- CreateView
- UpdateView
- DeleteView
- SearchView
- ArchiveView
- YearArchiveView, MonthArchive

## Полный CRUD

views
```python

from django.view.generic import (ListView, DetailView, CreateView, UpdateView, DeleteView)
from django.urls import reverse_lazy
from .models import Article

# Список
class ArticleListView(ListView):
    model = Article
    paginate_by = 10

# Детали
class ArticleDetailView(DetailView):
    model = Article

# Создание
class ArticleCreateView(CreateLiew):
    model = Article
    fields = ['title', 'content', 'category']
    success_url = reverse_lazy('article_list')

# Редактирование
class ArticleUpdateView(UpdateView):
    model = Article
    fields = ['title', 'content', 'category']
    success_url = reverse_lazy('article_list')

# Удаление
class ArticleDeleteView(DeleteView):
    model = Article
    success_url = reverse_lazy('article_list')
```

urls
```python
urlpatterns = [
    path('articles/', ArticleListView.as_view(), name='article_list'),
    path('articles/<int:pk>', ArticleListView.as_view(), name='article_detail'),
    path('articles/new/', ArticleCreateView.as_view(), name='article_create'),
    path('articles/<int:pk>/edit/', ArticleUpdateView.as_view(), name='article_update'),
    path('articles/<int:pk>/delete/', ArticleDeleteView.as_view(), name='article_delete'),
]
```

## Пример расширенной настройки
```python
class ArticleListView(ListView):
    model = Article
    context_object_name = 'articles'
    paginate_by = 10
    template_name = 'articles/list.html'

    def get_queryset(self):
        """Фильтрация + поиск"""

        # queryset - данные

        queryset = Article.objects.filter(published=True)
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(title__icontains=search)
        return queryset.order_by('-created_at')

    def get_context_data(self, **kwargs):
        """Дополнительный контекст"""

        # context - словарь для шаблона

        # 1. Категории для фильтра
        context['categories'] = Category.objects.all()
        
        # 2. Поисковый запрос
        context['search_query'] = self.request.GET.get('search', '')
        
        # 3. Статистика
        context['total_articles'] = Article.objects.filter(published=True).count()
        
        # 4. Рекомендации
        context['recommended'] = Article.objects.filter(
            category__popular=True
        )[:3]
        
        return context
```

**разница context и queryset**
```python
queryset  =  "коробка с яблоками"  (данные)
context   =  "поднос с коробкой + вилка + салфетка"  (данные + допы)

Шаблон видит только поднос (context)!
```

Пример
```python

class ArticleListView(ListView):
    model = Article
    template_name = 'articles/list.html'
    
    # 1. context_object_name - ИМЯ переменной в шаблоне (вместо object_list)
    context_object_name = 'articles'
    
    # 2. queryset - кастомный QuerySet
    queryset = Article.objects.filter(published=True).order_by('-created_at')
    
    # 3. paginate_by - пагинация
    paginate_by = 10
    paginate_orphans = 2
    
    # 4. get_queryset() - динамический queryset
    def get_queryset(self):
        queryset = super().get_queryset()
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(title__icontains=search)
        return queryset

```

Пример с фильтрацией и поиском
```python
class ArticleListView(ListView):
    model = Article
    template_name = 'articles/list.html'
    context_object_name = 'articles'
    paginate_by = 10
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('search', '')
        return context
    
    def get_queryset(self):
        queryset = Article.objects.all()
        search = self.request.GET.get('search')
        category = self.request.GET.get('category')
        
        if search:
            queryset = queryset.filter(
                models.Q(title__icontains=search) |
                models.Q(content__icontains=search)
            )
        
        if category:
            queryset = queryset.filter(category__slug=category)
            
        return queryset.order_by('-created_at')
```

Пример с вебинара
```python
from django.shortcuts import get_object_or_404
from .models import Author

class AuthorList(ListView):
    model = Author
    context_object_name = 'Authors'
    template_name = 'newapp/authors.html'

    def get_queryset(self):
        self.authorUser = get_object_or_404(Author, name=self.args[0])
        return Author.objects.filter(authorUser=self.authorUser)
```


















# Типы импортов

![alt text](image-15.png)

![alt text](image-16.png)

![alt text](image-17.png)


## Правила использования импортов

1. From-импорт конкретных объектов (80% случаев) - неквалифицированное обращение

```python
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView
from .models import Article, Category

def view(request):
    return render(request, 'template.html')
```

2. Утилиты, логирование, конфиг - прямое обращение
```python
import logging
import os
from pathlib import Path

logger = logging.getLogger(__name__)
```

3. Относительный импорты - внутри приложения



# get_absolute_url
Метод `get_absoulte_url()` - это стандартный способ получения полного URL для модели. Он возвращает абсолютный URL (с доменом и протоколом), который можно использовать для ссылок, RSS, API и т.д.

1. Метод должен быть определён в модели и возвращать строку с абсолютным URL
```python
from django.urls import reverse
from django.db import models

class Article(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200)

    def get_absoulte_url(self):
        # Возвращает полный URL для конкретного экземпляра
        return reverse('article_detail', kwargs={'slug': self.slug})
```

Комментарий: `article_detail` - это имя URL-паттерна (name). Reverse ищет только по имени. 

В файле urls.py
```python
urlpatterns = [
    # article_detail - это имя URL (name='article_detail')
    path('articles/<slug:slug>/',
        ArticleDetailView.as_view(),
        name='article_detail'),  # Это имя URL
]
```


2. Автоматическая работа Django Admin
Django Admin автоматически использует этот метод
```python
"View on site" -> https://example.com/articles/my-article
```

3. Пример использования
**Вью**
```python
def article_list(request):
    articles = Article.objects.all()
    return render(request, 'articles.html', context={'articles': articles})
```


**Шаблон**
```html
<!-- Получаем URL для каждой статьи -->
<a href="{{ article.get_absolute_url }}">{{ article.title }}</a>

<!-- Список статей -->
{% for article in articles %}
    <li><a href="{{ article.get_absolute_url }}">{{ article.title }}</li>
{% endfor %}
```

3. Пример использования во вью c классом (спорно)
```python
class ArticleCreateView(CreateView):
    model = Article
    fields = ['title', 'slug', 'content']

    def get_success_url(self):
        # Возвращаем URL новосозданной статьи!
        new_article = self.object
        return new_article.get_absoulute_url()
```

## Варианты реализации
1. ID
```python
def get_absolute_url(self):
    return reverse('article_detail', kwargs={'pk': self.pk})
```

2. slug
```python
def get_absolute_url(self):
    return reverse('article_detail', kwargs={'slug': self.slug})
```

3. С дополнительными параметрами
```python
def get_absolute_url(self):
    return reverse('article_detail', kwargs={
        'year': self.pub_date.year,
        'month': self.pub_date.month,
        'slug': self.slug
    })
```



 