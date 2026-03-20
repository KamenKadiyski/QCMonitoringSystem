from django.urls import path

from jobs.views import CreateJobView, DeleteJobView, JobListView, UpdateJobView

app_name = 'jobs'

urlpatterns = [
    path('create/', CreateJobView.as_view(), name='create_job'),
    path('list/', JobListView.as_view(), name='list_jobs'),
    path('update/<int:pk>/', UpdateJobView.as_view(), name='update_job'),
    path('delete/<int:pk>/', DeleteJobView.as_view(), name='delete_job'),


]
