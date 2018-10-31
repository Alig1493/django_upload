from django.urls import path

from django_file_upload.capacity.views import MachineDayView, SAHView, PcsView, GGPcsView

app_name = "capacity"

urlpatterns = [
    path('machine-day/', MachineDayView.as_view(), name='machine_day'),
    path('sah/', SAHView.as_view(), name='sah'),
    path('pcs/', PcsView.as_view(), name='pcs'),
    path('ggpcs/', GGPcsView.as_view(), name='ggpcs'),
]
