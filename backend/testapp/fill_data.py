# fill_data.py
import os
import sys
import django

# Настройка пути к проекту
sys.path.append('.')  # текущая директория
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from datetime import date
from testapp.models import People, HistLpu, Lpu, T001, T007

# Очистка
HistLpu.objects.all().delete()
People.objects.all().delete()
Lpu.objects.all().delete()
T001.objects.all().delete()
T007.objects.all().delete()

# Заполнение LPU
Lpu.objects.create(code='750066', caption='ГУЗ Читинская ЦРБ', bossname='Емельянов Геннадий Константинович')
Lpu.objects.create(code='750145', caption='ГУЗ КМЦ', bossname='Рыкова Наталья Ивановна')
Lpu.objects.create(code='750144', caption='ГУЗ ДКМЦ', bossname='Нардина Ирина Владимировна')
Lpu.objects.create(code='750004', caption='ГУЗ КБ №3', bossname='Горяев Николай Ильич')
Lpu.objects.create(code='750001', caption='ГУЗ Краевая клиническая больница', bossname='Шальнев Виктор Александрович')

# Заполнение T001
T001.objects.create(mcod='750066', nam_mo='Новотроицкая амбулатория', nom_podr='1')
T001.objects.create(mcod='750066', nam_mo='Участковая больница села Бургень', nom_podr='2')
T001.objects.create(mcod='750145', nam_mo='Поликлиническое подразделение №1', nom_podr='1')
T001.objects.create(mcod='750145', nam_mo='Поликлиническое подразделение №3', nom_podr='3')
T001.objects.create(mcod='750144', nam_mo='Поликлиническое подразделение №1', nom_podr='1')
T001.objects.create(mcod='750004', nam_mo="Поликлиника пгт.Первомайск", nom_podr='1')

# Заполнение T007
T007.objects.create(code_mo='750066', name_depth='Терапевтический участок', nom_podr='1', depth='1')
T007.objects.create(code_mo='750066', name_depth='Педиатрический участок', nom_podr='2', depth='2')
T007.objects.create(code_mo='750145', name_depth='Участок №1', nom_podr='1', depth='1')
T007.objects.create(code_mo='750145', name_depth='Участок №3', nom_podr='3', depth='3')
T007.objects.create(code_mo='750145', name_depth='Участок №10', nom_podr='3', depth='10')
T007.objects.create(code_mo='750144', name_depth='Участок №1', nom_podr='1', depth='2')
T007.objects.create(code_mo='750004', name_depth="Педиатрический участок №2", nom_podr='1', depth='4')

# Заполнение PEOPLE
p1 = People.objects.create(enp='7594045746370284', fam='ИВАНОВ', im='ИВАН', ot='ИВАНОВИЧ', w=1, dr=date(1960,1,1))
p2 = People.objects.create(enp='7594045584245684', fam='ПЕТРОВ', im='ПЁТР', ot='ПЕТРОВИЧ', w=1, dr=date(1990,7,7), lpu='750145', lpudt=date(2020,1,1), lpudx=date(2020,7,1), lpuuch='5')
p3 = People.objects.create(enp='7594045746375674', fam='СЕЛИНА', im='ЛЮБОВЬ', ot='ИЛЬИНИЧНА', w=2, dr=date(1968,5,4), lpu='750066')
p4 = People.objects.create(enp='7594045746370000', fam='ТОМСКИХ', im='ИРИНА', ot='СЕРГЕЕВНА', w=2, dr=date(2002,12,5), lpu='750145', lpudt=date(2020,1,1), lpuuch='10')
p5 = People.objects.create(enp='7594029345746370', fam='ДОНДОКОВ', im='ТИМУР', ot='', w=1, dr=date(2018,2,16), lpu='750144', lpudt=date(2018,3,1), lpuuch='2')

# Заполнение HISTLPU
HistLpu.objects.create(pid=p2, lpu='750145', lpudt=date(2020,1,1), lpudx=date(2020,7,1), district='5', subdiv='1')
HistLpu.objects.create(pid=p3, lpu='750066', lpudt=None, lpudx=None, district='', subdiv='')
HistLpu.objects.create(pid=p4, lpu='750145', lpudt=date(2019,1,1), lpudx=date(2019,12,31), district='3', subdiv='3')
HistLpu.objects.create(pid=p4, lpu='750145', lpudt=date(2020,1,1), lpudx=None, district='3', subdiv='10')
HistLpu.objects.create(pid=p5, lpu='750144', lpudt=date(2018,3,1), lpudx=None, district='1', subdiv='2')

print('Данные загружены!')