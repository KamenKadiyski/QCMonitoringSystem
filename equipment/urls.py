from django.urls import path

import equipment
from equipment import views

app_name = 'equipment'

urlpatterns = [
    path('machine/upload/', equipment.views.MachineUploadView.as_view(), name='machine_upload'),
    path('tool/upload/', equipment.views.ToolUploadView.as_view(), name='tool_upload'),


]