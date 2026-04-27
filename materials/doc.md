- Миграции - файлы для настройки базы данных, которые указывают базе, как и какая информация будет в ней хранится.
- asgiref Поддержка асинхронности (ASGI)
- pkg-resources	- Управление метаданными пакетов (часть setuptools)
- pytz - Работа с часовыми поясами
- setuptools - Сборка и установка пакетов
- sqlparse - Анализ и форматирование SQL‑запросов


- csrf token - CSRF (Cross-Site Request Forgery) — атака, когда злоумышленник заставляет авторизованного пользователя выполнить нежелательное действие.

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



 