from django.shortcuts import get_object_or_404
from django.urls.base import reverse_lazy, reverse
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView

from jobs.forms import CreateJobForm
from jobs.models import Job


# Create your views here.
class CreateJobView(CreateView):
    model = Job
    form_class = CreateJobForm
    template_name = 'jobs/create_job.html'
    success_url = reverse_lazy('jobs:list_jobs')
    page_title = 'Add details for the job'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                'page_title': self.page_title,


            }
        )
        return context

class JobListView(ListView):
    model = Job
    template_name = 'jobs/list_jobs.html'
    page_title='List of Jobs'

    def get_queryset(self):
        jobs = Job.objects.all().order_by('job_code')
        return jobs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        menu_items = [{
            'title': 'Add job',
            'url': reverse('jobs:create_job'),
            'icon': 'journal-check',
            'color': 'text-primary'
        }, {
            'title': 'Home',
            'url': reverse('accounts:home'),
            'icon': 'briefcase',
            'color': 'text-primary'
        }]
        context.update(
            {
                'page_title': self.page_title,
                'menu_items': menu_items,
            }
        )
        return context




class UpdateJobView(UpdateView):
    model = Job


class DeleteJobView(DeleteView):
    model = Job
