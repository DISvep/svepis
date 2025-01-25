from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.views.generic import ListView, CreateView, View, DeleteView
from django.http import JsonResponse
from django.urls import reverse_lazy
from .models import Widget
from .forms import WidgetForm


class PortalEditorView(LoginRequiredMixin, ListView):
    model = Widget
    template_name = 'redactor.html'
    context_object_name = 'widgets'

    def get_queryset(self):
        return Widget.objects.filter(user=self.request.user)


class WidgetCreateView(LoginRequiredMixin, CreateView):
    model = Widget
    form_class = WidgetForm
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('portal', kwargs={'pk': self.request.user.portal.pk})
    
    
class WidgetUpdatePositionView(LoginRequiredMixin, View):
    def post(self, request, widget_id):
        widget = get_object_or_404(Widget, id=widget_id, user=request.user)
        try:
            data = request.POST
            widget.x_position = data.get('x_position', widget.x_position)
            widget.y_position = data.get('y_position', widget.y_position)
            widget.save()
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=400)


class WidgetUpdateView(LoginRequiredMixin, View):
    def post(self, request, widget_id):
        widget = get_object_or_404(Widget, id=widget_id, user=request.user)
        try:
            data = request.POST
            widget.width = data.get('width', widget.width)
            widget.height = data.get('height', widget.height)
            widget.z_index = data.get('z_index', widget.z_index)
            widget.save()
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=400)
            
            
class WidgetDeleteView(LoginRequiredMixin, DeleteView):
    model = Widget
    
    def get_success_url(self):
        return reverse_lazy('portal', kwargs={'pk': self.request.user.portal.pk})
    