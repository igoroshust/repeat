from django.shortcuts import render
from django.http import JsonResponse
from datetime import datetime
from .models import People, HistLpu, Lpu, T001, T007

import pprint

def check_attachment(request):
    """Проверка прикрепления к мед.организации"""
    
    context = {'result': None}
    
    # Получаем параметры из GET-запроса
    input_enp = request.GET.get('enp', '').strip()
    input_fam = request.GET.get('fam', '').strip()
    input_im = request.GET.get('im', '').strip()
    input_ot = request.GET.get('ot', '').strip()
    input_dr = request.GET.get('dr', '').strip()
    
    # 1. Поиск человека: либо по ЕНП, либо по ФИО + дата рождения
    person = None
    
    if input_enp:
        # Поиск по номеру полиса
        person = People.objects.filter(enp=input_enp).first()
        
    elif input_fam and input_ot and input_im and input_dr:
        # Поиск по ФИО и дате рождения
        try:
            dr_date = datetime.strptime(input_dr, "%d.%m.%Y").date()
            person = People.objects.filter(
                fam__iexact=input_fam,
                im__iexact=input_im,
                ot__iexact=input_ot,
                dr=dr_date
            ).first()
        except ValueError:
            pass
    
    # 2. Человек не найден
    if not person:
        context['result'] = {
            'status': 'not_found',
            'message': 'Такой полис не найден'
        }
        return render(request, 'check_attachment.html', context)
    
    # 3. Человек найден — проверяем статус прикрепления
    result = {
        'person': {
            'fio': f"{person.fam} {person.im} {person.ot}".strip(),
            'dr': person.dr.strftime('%d.%m.%Y')
        },
        'status': None,
        'lpu': None,
        'subdiv': None,
        'district': None
    }
    
    # Правило: если lpu не заполнено или заполнено lpudx → не прикреплён
    if not person.lpu:
        result['status'] = 'not_attached'
        result['message'] = 'не прикреплен(-a)'
        
    elif person.lpudx:
        result['status'] = 'not_attached'
        result['message'] = 'не прикреплён(-a)'
        
    else:
        # 4. Прикреплён — ищем название ЛПУ
        lpu_obj = Lpu.objects.filter(code=person.lpu).first()
        result['lpu'] = lpu_obj.caption if lpu_obj else "Неизвестная мед.орг."
        
        # Ищем детализацию в HISTLPU (текущая запись без даты открепления)
        hist = HistLpu.objects.filter(
            pid=person,
            lpu=person.lpu,
            lpudx__isnull=True
        ).order_by('-lpudt').first()
        
        if hist:
            # Подразделение (T001)
            if hist.district:
                district = T001.objects.filter(
                    mcod=person.lpu,
                    nom_podr=hist.district
                ).first()
                result['district'] = district.nam_mo if district else None
                
            # Участок (T007)
            if hist.subdiv:
                subdiv = T007.objects.filter(
                    code_mo=person.lpu,
                    depth=hist.subdiv
                ).first()
                result['subdiv'] = subdiv.name_depth if subdiv else None
        
        result['status'] = 'attached'
        
        # Формируем сообщение
        msg_parts = [f"прикреплен(-a) к {result['lpu']}"]
        if result['district']:
            msg_parts.append(result['district'])
        if result['subdiv']:
            msg_parts.append(result['subdiv'])
        result['message'] = ', '.join(msg_parts)
    
    context['result'] = result
    
    print('result:', result)
    return render(request, 'check_attachment.html', context)