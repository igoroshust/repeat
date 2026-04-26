## Плюсы и минусы Django

![alt text](image.png)

## apps.py
apps.py - файл конфигурации приложения Django. Содержит класс конфигурации (AppConfig), который задаёт метаданные и настройки приложения, а также позволяет вмешаться в процесс запуска Django.

Нужен для:
- структурированной информации в приложении
- безопасного выполнения инициализационного кода
- интеграции с Django без циклических зависимостей
- тонкой настройки поведения приложения в проекте


# Созадние моделей 

## Промежуточная таблица

![alt text](image-1.png)


## Модель Post

![alt text](image-2.png)

## update rating

![alt text](image-5.png)

## Обращение к связанным полям

![alt text](image-6.png)

## Вывод пользователя с самым низким рейтингом

![alt text](image-7.png)

## Пример промежуточной модели
```python
from django.db import models
from datetime import date

class Employee(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Project(models.Model):
    title = models.CharField(max_length=200)
    employees = models.ManyToManyField(
        Employee,
        through='Assignment'  # Указываем промежуточную модель
    )

    def __str__(self):
        return self.title

class Assignment(models.Model):  # Промежуточная модель
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    date_assigned = models.DateField(default=date.today)
    role = models.CharField(max_length=50, default='Participant')

    class Meta:
        unique_together = ('employee', 'project')  # Уникальность связки

    def __str__(self):
        return f"{self.employee} in {self.project} as {self.role}"
```

## Заменить дефолтный primary key

![alt text](image-8.png)

## self в моделях

![alt text](image-9.png)

## Типы полей

![alt text](image-10.png)

## Лучшая практика комбинирования шаблонов

![alt text](image-11.png)

## null=True vs blank=True

![alt text](image-12.png)

![alt text](image-13.png)

## Пример моделей боевого проекта

![alt text](image-14.png)