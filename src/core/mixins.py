class PartialUpdateMixin:
    """
    Mixin used for partial model update.
    """
    def update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return super().update(request, *args, **kwargs)
