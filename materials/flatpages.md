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
```html
<!DOCTYPE html>
<html>
<head>
<title>{{ flatpage.title }}</title>
</head>
<body>
    <h2>{{ flatpage.title }}</h2>
    <hr>
    <h3>Наши контакты:</h3>
    {{ flatpage.content }}
</body>
</html>
```s

### 5. Заполняем данные в админке
1. Переходим по адресу http://127.0.0.1:8000/admin/
2. В разделе flatpages заполняем содержимое по типу:
```python
URL: /about/test/
...
Template name: flatpages/index.html
```

### При переходе по адресу http://127.0.0.1:8000/flatpages/about/test теперь отображается страница с index.html





# Дополнительно

### Как Django понимает работу с контектом flatpage

```python
class FlatpageView(TemplateView):
    def get(self, request, url):
        # 1. Находит Flatpage по URL
        flatpage = get_object_or_404(
            Flatpage.objects.select_related('sites').filter(
                url_exact=url,
                sites__id=settings.SITE_ID,
            )
        )
        
        # 2. Проверки
        if flatpage.registration_required and not request.user.is_authenticated:
            return redirect(settings.LOGIN_URL)
            
        # 3. Определяет шаблон
        template_name = flatpage.template_name or 'flatpages/default.html'
        
        # 4. Создает контекст
        context = self.get_context_data(
            flatpage=flatpage,      # ← ВОТ ОН!
            request=request,
        )
        
        return self.render_to_response(context, template_name)
```