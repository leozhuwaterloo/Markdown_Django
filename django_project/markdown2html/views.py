from .forms import NoteForm, CourseForm, NoteContentForm
from .models import Note, Course
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import get_object_or_404


# Course
class CourseView(generic.ListView):
    template_name = "markdown2html/courses.html"
    context_object_name = 'courses'

    def get_queryset(self):
        return Course.objects.order_by('-publish')


class CourseDetailView(generic.DetailView):
    model = Course
    template_name = 'markdown2html/notes.html'
    slug_url_kwarg = "course_slug"
    slug_field = "course_slug"

    def get_context_data(self, **kwargs):
        context = super(CourseDetailView, self).get_context_data(**kwargs)
        context['notes'] = context["course"].note_set.all().order_by('-publish')
        return context


class CourseCreate(CreateView):
    model = Course
    form_class = CourseForm


class CourseDelete(DeleteView):
    model = Course
    success_url = reverse_lazy('markdown2html:index')
    slug_url_kwarg = "course_slug"
    slug_field = "course_slug"

    def get_context_data(self, **kwargs):
        context = super(CourseDelete, self).get_context_data(**kwargs)
        context['course'] = get_object_or_404(Course, course_slug=self.kwargs.get('course_slug'))
        return context


class CourseUpdate(UpdateView):
    model = Course
    form_class = CourseForm
    template_name_suffix = '_update_form'
    slug_url_kwarg = "course_slug"
    slug_field = "course_slug"

    def get_context_data(self, **kwargs):
        context = super(CourseUpdate, self).get_context_data(**kwargs)
        context['course'] = get_object_or_404(Course, course_slug=self.kwargs.get('course_slug'))
        return context

    def get_success_url(self):
        return reverse_lazy('markdown2html:index')


# Note
class NoteDetailView(generic.DetailView):
    model = Note
    template_name = 'markdown2html/note_detail.html'
    slug_url_kwarg = "note_slug"
    slug_field = "note_slug"

    def get_context_data(self, **kwargs):
        context = super(NoteDetailView, self).get_context_data(**kwargs)
        note_instance = get_object_or_404(Note, note_slug=self.kwargs.get('note_slug'))
        note_set = context["note"].course.note_set.all().order_by('publish')
        context['theorem_counter'] = get_order(note_instance, note_set)
        return context


def get_order(instance, ordered_set):
    for i in range(0, ordered_set.count()):
        if instance.id == ordered_set[i].id:
            return i+1
    return 0


class NoteCreate(CreateView):
    model = Note
    form_class = NoteForm

    def form_valid(self, form):
        course = get_object_or_404(Course, course_slug=self.kwargs.get('course_slug'))
        form.instance.course = course
        return super(CreateView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(NoteCreate, self).get_context_data(**kwargs)
        context['course'] = get_object_or_404(Course, course_slug=self.kwargs.get('course_slug'))
        return context


class NoteDelete(DeleteView):
    model = Note
    slug_url_kwarg = "note_slug"
    slug_field = "note_slug"

    def get_success_url(self):
        return reverse_lazy('markdown2html:course_detail', kwargs={'course_slug': self.kwargs.get("course_slug")})

    def get_context_data(self, **kwargs):
        context = super(NoteDelete, self).get_context_data(**kwargs)
        context['note'] = get_object_or_404(Note, note_slug=self.kwargs.get('note_slug'))
        return context


class NoteUpdate(UpdateView):
    model = Note
    form_class = NoteForm
    template_name_suffix = '_update_form'
    slug_url_kwarg = "note_slug"
    slug_field = "note_slug"

    def get_context_data(self, **kwargs):
        context = super(NoteUpdate, self).get_context_data(**kwargs)
        context['note'] = get_object_or_404(Note, note_slug=self.kwargs.get('note_slug'))
        return context

    def get_success_url(self):
        return reverse_lazy('markdown2html:course_detail', kwargs={'course_slug': self.kwargs.get("course_slug")})


class NoteContentUpdate(UpdateView):
    model = Note
    form_class = NoteContentForm
    template_name_suffix = '_content_update_form'
    slug_url_kwarg = "note_slug"
    slug_field = "note_slug"

    def get_context_data(self, **kwargs):
        context = super(NoteContentUpdate, self).get_context_data(**kwargs)
        context['note'] = get_object_or_404(Note, note_slug=self.kwargs.get('note_slug'))
        return context
