from django.urls import path
from .views import WidgetCreateView, WidgetUpdatePositionView, WidgetUpdateView, WidgetDeleteView


urlpatterns = [
    path('add-widget/', WidgetCreateView.as_view(), name="add-widget"),
    path('update-widget-position/<int:widget_id>', WidgetUpdatePositionView.as_view(), name="update-widget-position"),
    path('update-widget/<int:widget_id>', WidgetUpdateView.as_view(), name='update-widget'),
    path('delete-widget/<int:pk>', WidgetDeleteView.as_view(), name='delete-widget')
]
