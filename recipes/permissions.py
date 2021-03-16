from django.shortcuts import redirect


class AdminAuthorPermission:
    def dispatch(self, request, *args, **kwargs):
        if (self.request.user.is_superuser
                or self.request.user.is_admin
                or self.request.user.username == self.kwargs['username']):
            return super().dispatch(request, *args, **kwargs)
        return redirect(
            'recipes:recipe',
            username=self.kwargs['username'],
            pk=self.kwargs['pk'],
        )
