from django.urls import path

from .views import AddToQCLogView, JobLogListView, UpdateQCLogView

app_name = 'qcloging'

urlpatterns = [
    path('', JobLogListView.as_view(), name='list_qc_logs'),
    path('add_to_qc_log/', AddToQCLogView.as_view(), name='add_qc_log'),
    path('qc/update/<int:pk>/', UpdateQCLogView.as_view(), name='update_qc_log'),



]
