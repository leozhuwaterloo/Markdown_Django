from .models import Course


def add_variable_to_context(request):
    return {
        'global_courses': Course.objects.all(),
    }
