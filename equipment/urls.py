from django.urls import path

import equipment
from equipment import views

app_name = 'equipment'

urlpatterns = [
    path('', equipment.views.CombinedEquipmentView.as_view(), name='combined_equipment'),

    path('machine/upload/', equipment.views.MachineUploadView.as_view(), name='machine_upload'),
    path('tool/upload/', equipment.views.ToolUploadView.as_view(), name='tool_upload'),


]