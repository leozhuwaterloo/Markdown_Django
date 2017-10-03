import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_project.settings")

from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()

from markdown2html.models import *
from datetime import date

from django.conf import settings


def get_file_text(file):
    with open(file) as fp:
        return fp.read()


def load_notes(contributor="Lichen Zhu", publish=date.today()):
    for course in os.listdir(settings.MEDIA_ROOT):
        temp_course = Course(title=course.upper(), contributor=contributor,
                             publish=publish)
        temp_course.save()
        print("Loaded Course: " + course)
        for note in os.listdir(settings.MEDIA_ROOT + "/" + course):
            print("Loaded Note: " + note)
            file = course + '/' + note
            temp_note = Note(course=temp_course, title=note.replace('.md', ''),
                             content=get_file_text(settings.MEDIA_ROOT + '/' + file),
                             content_file=file, contributor=contributor,
                             publish=publish)
            temp_note.save()


load_notes()
