from django.core.exceptions import PermissionDenied


class IsChatMember(object):
    def dispatch(self, request, *args, **kwargs):
        try:
            Model = self.get_object()
            
            if (
                self.request.user not in Model.members.all()
                and not self.request.user.is_superuser
            ):
                raise PermissionDenied("You dont have a permission.")
        except:
            if (
                not self.request.user.is_superuser
            ):
                raise PermissionDenied("You dont have a permission.")
        
        return super().dispatch(request, *args, **kwargs)
