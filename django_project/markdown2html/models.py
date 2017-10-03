import shutil
from django.conf import settings
from django.core.files.base import ContentFile
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models.signals import post_delete
from django.dispatch.dispatcher import receiver
from django.utils.html import mark_safe
from django.utils.text import slugify
from markdown_deux import markdown
from markdown2html import uwaterlooapi_django


# Courses
class Course(models.Model):
    title = models.CharField(max_length=250)
    description = models.CharField(max_length=250)
    contributor = models.CharField(max_length=250)
    publish = models.DateField(auto_now=False, auto_now_add=False)
    course_slug = models.SlugField(unique=True)

    def __str__(self):
        return self.title + "-" + self.contributor

    def get_absolute_url(self):
        return reverse('markdown2html:course_detail', kwargs={'course_slug': self.course_slug, })

    def save(self, *args, **kwargs):
        if self.course_slug == "":
            self.course_slug = create_course_slug(self)
        splited = self.title.replace('-', ' ').split(' ')
        if len(splited) >= 2:
            self.description = uwaterlooapi_django.find_course(splited[0], int(splited[1]))
        else:
            self.description = uwaterlooapi_django.error
        super(Course, self).save(*args, **kwargs)


def create_course_slug(instance, new_slug=None):
    slug = slugify(instance.title)
    if slug == "create" or slug == "course" or slug == "update" or slug == "delete" or slug == "note" or slug == "notes":
        slug += "-0"

    if new_slug is not None:
        slug = new_slug
    qs = Course.objects.filter(course_slug=slug).order_by("-id")
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" % (slug, qs.first().id)
        return create_note_slug(instance, new_slug=new_slug)
    return slug


# Note
def note_slug_directory_path(instance, filename):
    return instance.course.course_slug + "/" + instance.note_slug + ".md"


class Note(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.CharField(max_length=250)
    content = models.TextField()
    content_file = models.FileField(blank=True, upload_to=note_slug_directory_path)
    contributor = models.CharField(max_length=250)
    publish = models.DateField(auto_now=False, auto_now_add=False)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    note_slug = models.SlugField(unique=True)

    def __str__(self):
        return self.title + "-" + self.contributor

    def get_absolute_url(self):
        return reverse('markdown2html:note_detail',
                       kwargs={'course_slug': self.course.course_slug, 'note_slug': self.note_slug, })

    def get_file_text(self):
        with open(self.content_file.path) as fp:
            return fp.read()

    def save(self, *args, **kwargs):
        if self.note_slug == "":
            self.note_slug = create_note_slug(self)

        if self.content_file == "":
            self.content_file.save(self.note_slug + ".md", ContentFile(''))
            return
        else:
            try:
                self.get_file_text()
            except FileNotFoundError:
                super(Note, self).save(*args, **kwargs)
                self.content = self.get_file_text()

            self.content = self.content.replace('\r', '')
            # print(self.content.split("\n"))
            # print(self.get_file_text().split("\n"))
            if self.content != self.get_file_text():
                self.content_file = ""
                self.content_file.save(self.note_slug + ".md",
                                       ContentFile(self.content))

        super(Note, self).save(*args, **kwargs)

    def get_markdown(self):
        return mark_safe(markdown(self.content))


def create_note_slug(instance, new_slug=None):
    slug = slugify(instance.title)
    if slug == "create" or slug == "course" or slug == "update" or slug == "delete" or slug == "note" or slug == "notes":
        slug += "-0"

    if new_slug is not None:
        slug = new_slug
    qs = Note.objects.filter(note_slug=slug).order_by("-id")
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" % (slug, qs.first().id)
        return create_note_slug(instance, new_slug=new_slug)
    return slug


@receiver(post_delete, sender=Course)
def note_directory_delete(sender, instance, **kwargs):
    try:
        shutil.rmtree(settings.MEDIA_ROOT + "\\" + instance.course_slug)
    except Exception:
        return
