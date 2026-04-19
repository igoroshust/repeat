## 1. Добавляем настройки (settings)
```python
import os

INSTALLED_APPS = [
    ...

    'django.contrib.sites',
    'django.contrib.flatpages',
]

MIDDLEWARE = [
    ...
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
]

SITE_ID = 1

TEMPLATES = {
    ...
    'DIRS': [os.path.join('BASE_DIR', 'templates')],
    ...
}
```

### 2. Указываем маршруты (urls)
```python
from django.urls import path, include

urlpatterns = [
    ...
    path('flatpages/', include('django.contrib.flatpages.urls')),
]
```

### 3. Применяем миграции
```python
python manage.py migrate
```

### 4. Создаём шаблоны
Внутри приложения appname создаём templates -> flatpages -> index.html
Заполняем содержимым html-документ

### 5. Заполняем данные в админке
1. Переходим по адресу http://127.0.0.1:8000/admin/
2. В разделе flatpages заполняем содержимое по типу:
```python
URL: /about/test/
...
Template name: flatpages/index.html
```

### При переходе по адресу http://127.0.0.1:8000/flatpages/about/test теперь отображается страница с index.html