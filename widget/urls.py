from django.urls import path
from .views import PortalEditorView, WidgetCreateView, WidgetUpdatePositionView


urlpatterns = [
    path('redactor/', PortalEditorView.as_view(), name='redactor'),
    path('add-widget/', WidgetCreateView.as_view(), name="add-widget"),
    path('update-widget-position/<int:widget_id>', WidgetUpdatePositionView.as_view(), name="update-widget-position")
]
