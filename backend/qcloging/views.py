from django.views.generic import CreateView, ListView, UpdateView
from django import forms
from rest_framework.reverse import reverse_lazy

from .models import QCLog


# Create your views here.
class JobLogListView(ListView):
    model = QCLog
    template_name = 'qcloging/list_qc_logs.html'
    page_title = 'Списък QC Логове'

    def get_queryset(self):
        queryset = QCLog.objects.select_related('job_log', 'qc_inspector').all().order_by('-logged_at')
        date_query = self.request.GET.get('date_filter')

        if date_query:

            queryset = queryset.filter(logged_at__date=date_query)
        return queryset


class AddToQCLogView(CreateView):
    model = QCLog
    fields = '__all__'
    template_name = 'qcloging/add_to_qc_log.html'
    success_url = reverse_lazy('qcloging:list_qc_logs')

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        for name, field in form.fields.items():
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs.update({'class': 'form-check-input'})
            else:
                field.widget.attrs.update({'class': 'form-control'})
        return form




class UpdateQCLogView(UpdateView):
    model = QCLog
    fields = '__all__'
    template_name = 'qcloging/update_qc_log.html'
    success_url = reverse_lazy('qcloging:list_qc_logs')

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        for name, field in form.fields.items():
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs.update({'class': 'form-check-input'})
            else:
                field.widget.attrs.update({'class': 'form-control'})
        return form
