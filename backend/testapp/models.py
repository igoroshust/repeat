from django.db import models
from django.db.models import Q

class People(models.Model):
    """Основная таблица с персональными данными"""
    enp = models.CharField(max_length=16, unique=True, verbose_name='ЕНП (полис)')
    fam = models.CharField(max_length=40, verbose_name='Фамилия')
    im = models.CharField(max_length=40, verbose_name='Имя')
    ot = models.CharField(max_length=40, blank=True, verbose_name='Отчество')
    w = models.SmallIntegerField(verbose_name='Пол (1-м, 2-ж)')
    dr = models.DateField(verbose_name='Дата рождения')
    
    # Поля прикрепления
    lpu = models.CharField(max_length=6, blank=True, verbose_name='Код мед.орг.')
    lpudt = models.DateField(null=True, blank=True, verbose_name='Дата прикрепления')
    lpudx = models.DateField(null=True, blank=True, verbose_name='Дата открепления')
    lpuuch = models.CharField(max_length=10, blank=True, verbose_name='Код участка (устарел)')

    def __str__(self):
        return f"{self.fam} {self.im} {self.ot}"

class HistLpu(models.Model):
    """История прикрепления"""
    pid = models.ForeignKey(People, on_delete=models.CASCADE, related_name='history')
    lpu = models.CharField(max_length=6, verbose_name='Код мед.орг.')
    lpudt = models.DateField(null=True, blank=True, verbose_name='Дата прикрепления')
    lpudx = models.DateField(null=True, blank=True, verbose_name='Дата открепления')
    district = models.CharField(max_length=10, blank=True, verbose_name='Код участка')
    subdiv = models.CharField(max_length=10, blank=True, verbose_name='Код подразделения')

class Lpu(models.Model):
    """Справочник мед.организаций"""
    code = models.CharField(max_length=6, unique=True)
    caption = models.CharField(max_length=100, verbose_name='Название')
    bossname = models.CharField(max_length=150, verbose_name='Главврач')

class T001(models.Model):
    """Справочник подразделений"""
    mcod = models.CharField(max_length=6, verbose_name='Код мед.орг.')
    nam_mo = models.CharField(max_length=100, verbose_name='Наименование подразделения')
    nom_podr = models.CharField(max_length=10, verbose_name='Код подразделения в мед.орг.')

class T007(models.Model):
    """Справочник участков"""
    code_mo = models.CharField(max_length=6, verbose_name='Код мед.орг.')
    name_depth = models.CharField(max_length=100, verbose_name='Наименование участка')
    nom_podr = models.CharField(max_length=10, verbose_name='Код подразделения в мед.орг.')
    depth = models.CharField(max_length=10)