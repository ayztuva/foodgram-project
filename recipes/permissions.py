from django.shortcuts import redirect


class AdminAuthorPermission:
    """
        If user is not owner or admin -- just redirect him
        to current recipe page
    """

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
