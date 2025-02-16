from django.core.exceptions import PermissionDenied


class IsOwnerMixin(object):
    def dispatch(self, request, *args, **kwargs):
        try:
            Model = self.get_object()
            
            if (
                Model.user != self.request.user
                and not self.request.user.is_superuser
            ):
                raise PermissionDenied("You dont have a permission.")
        except:
            if (
                not self.request.user.is_superuser
            ):
                raise PermissionDenied('You dont have a permission.')
        
        return super().dispatch(request, *args, **kwargs)
    