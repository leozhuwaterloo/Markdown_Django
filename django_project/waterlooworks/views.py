from django.views import generic
from .models import Job
from django.shortcuts import render
from django.views.generic.edit import UpdateView


class JobsListView(generic.ListView):
    template_name = "waterlooworks/job_list.html"
    context_object_name = 'jobs'

    def get_queryset(self):
        return Job.objects.order_by('id')


class JobsDetailView(generic.DetailView):
    model = Job
    template_name = 'waterlooworks/job_detail.html'


def main_index(request):
    return render(request, 'waterlooworks/main_index.html')


class JobUpdateView(UpdateView):
    model = Job
    form_class = NoteContentForm
    template_name_suffix = '_content_update_form'
    slug_url_kwarg = "note_slug"
    slug_field = "note_slug"

    def get_context_data(self, **kwargs):
        context = super(NoteContentUpdate, self).get_context_data(**kwargs)
        context['note'] = get_object_or_404(Note, note_slug=self.kwargs.get('note_slug'))
        return context

