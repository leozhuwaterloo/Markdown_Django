    from django.conf.urls import url
from . import views

app_name = 'markdown2html'

urlpatterns = [
    url(r'^$', views.CourseView.as_view(), name="index"),

    # /course/create/
    url(r'^course/create/$', views.CourseCreate.as_view(), name='course_create'),
    # /<course_slug>/update
    url(r'^(?P<course_slug>[-\w]+)/update/$', views.CourseUpdate.as_view(), name='course_update'),
    # /<course_slug>/delete
    url(r'^(?P<course_slug>[-\w]+)/delete/$', views.CourseDelete.as_view(), name='course_delete'),
    # /<course_slug>/notes
    url(r'^(?P<course_slug>[-\w]+)/notes/$', views.CourseDetailView.as_view(), name='course_detail'),

    # /<course_slug>/<note_slug>/content/update
    url(r'^(?P<course_slug>[-\w]+)/(?P<note_slug>[-\w]+)/content/update/$', views.NoteContentUpdate.as_view(),
        name='note_content_update'),
    # /<course_slug>/note/create/
    url(r'^(?P<course_slug>[-\w]+)/note/create/$', views.NoteCreate.as_view(), name='note_create'),
    # /<course_slug>/<note_slug>/update
    url(r'^(?P<course_slug>[-\w]+)/(?P<note_slug>[-\w]+)/update/$', views.NoteUpdate.as_view(), name='note_update'),
    # /<course_slug>/<note_slug>/delete
    url(r'^(?P<course_slug>[-\w]+)/(?P<note_slug>[-\w]+)/delete/$', views.NoteDelete.as_view(), name='note_delete'),
    # /<course_slug>/<note_slug>/
    url(r'^(?P<course_slug>[-\w]+)/(?P<note_slug>[-\w]+)/$', views.NoteDetailView.as_view(), name='note_detail'),

]
