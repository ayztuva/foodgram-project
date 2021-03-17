from django.views.generic.base import TemplateView


class AuthorPage(TemplateView):
    template_name = 'flatpages/about.html'
    extra_context = {
        'title': 'Об авторе',
        'content_title': 'Об авторе сайта',
        'content': [
            'Иван Грибов',
            'github: @ayztuva',
            'email: evan.gribov@gmail.com',
        ]
    }

class TechPage(TemplateView):
    template_name = 'flatpages/about.html'
    extra_context = {
        'title': 'Технологии',
        'content_title': 'Список использованных технологий',
        'content': [
            'Python 3',
            'Django 3.1',
            'Django REST Framework 3',
            'PostgreSQL',
        ]
    }