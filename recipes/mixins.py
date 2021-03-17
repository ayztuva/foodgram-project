from .models import Tag


class TagContextMixin:
    @property
    def extra_context(self):
        return {
            'active_tags': self.request.GET.getlist('tags'),
            'tags': Tag.objects.all(),
        }
