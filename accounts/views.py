from django.shortcuts import render
from django.urls.base import reverse

import equipment


def home_view(request):
    user = request.user
    menu_items = []

    # 1. ОБЩОДОСТЪПНИ
    menu_items.append({
        'title': 'Въведи Скрап', 'url': '',
        'icon': 'recycle', 'color': 'text-success'
    })

    if user.is_authenticated:
        # Вземаме групите
        user_groups = list(user.groups.values_list('name', flat=True))

        # АКО Е SUPERUSER - добавяме всичко директно и връщаме резултата
        if user.is_superuser:
            menu_items.extend([
                {'title': 'QC Logging', 'url': reverse('jobs:list_jobs'), 'icon': 'journal-check', 'color': 'text-primary'},
                {'title': 'Jobs', 'url': reverse('jobs:list_jobs'), 'icon': 'briefcase', 'color': 'text-primary'},
                {'title': 'Trading Parties', 'url': '', 'icon': 'building', 'color': 'text-primary'},
                {'title': 'Accounts (HR)', 'url': '', 'icon': 'person-gear', 'color': 'text-info'},
                {'title': 'Materials', 'url': '', 'icon': 'box-seam', 'color': 'text-warning'},
                {'title': 'Equipment', 'url': reverse('equipment:combined_equipment'), 'icon': 'tools', 'color': 'text-warning'},
                {'title': 'Създай QC Issue', 'url': '', 'icon': 'exclamation-octagon', 'color': 'text-danger'},
                {'title': 'Job Log', 'url': '', 'icon': 'clipboard-data', 'color': 'text-secondary'},
            ])
            # Можем да спрем дотук, за да не минаваме през останалите проверки
            return render(request, 'shared/template.html', {'menu_items': menu_items})

        # 2. QC МЕНИДЖЪР
        if 'QC Manager' in user_groups:
            menu_items.extend([
                {'title': 'QC Logging', 'url': '', 'icon': 'journal-check', 'color': 'text-primary'},
                {'title': 'Jobs', 'url': reverse('jobs:list_jobs'), 'icon': 'briefcase', 'color': 'text-primary'},
                {'title': 'Trading Parties', 'url': '', 'icon': 'building', 'color': 'text-primary'},
            ])




        # 3. HR (Accounts CRUD)
        if 'HR' in user_groups:
            menu_items.append({'title': 'Accounts (HR)', 'url': '', 'icon': 'person-gear', 'color': 'text-info'})

        # 4. PRODUCTION MANAGER (Materials & Equipment)
        if 'Production Manager' in user_groups:
            menu_items.extend([
                {'title': 'Materials', 'url': '', 'icon': 'box-seam', 'color': 'text-warning'},
                {'title': 'Equipment', 'url': '', 'icon': 'tools', 'color': 'text-warning'},
            ])

        # 5. SUPERVISOR, QC INSPECTOR, TEAM LEADER (QC Issue Creation)
        special_roles = ['Supervisor', 'QC Inspector', 'Team Leader']
        if any(role in user_groups for role in special_roles):
            menu_items.append({'title': 'Създай QC Issue', 'url': '', 'icon': 'exclamation-octagon', 'color': 'text-danger'})

        # 6. COLOURMEN (JobLog & Скрап)
        if 'Colourmen' in user_groups:
            menu_items.append({'title': 'Job Log', 'url': '', 'icon': 'clipboard-data', 'color': 'text-secondary'})

    return render(request, 'shared/template.html', {'menu_items': menu_items})
