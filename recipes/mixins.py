from .models import Tag


class TagContextMixin:
    """Adding tags in context"""

    @property
    def extra_context(self):
        return {
            'active_tags': self.request.GET.getlist('tags'),
            'tags': Tag.objects.all(),
        }
