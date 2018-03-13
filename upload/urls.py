from django.urls import path

from upload.views import UploadView, FileListView

app_name = 'upload'

urlpatterns = [
    path('', FileListView.as_view(), name='files-list'),
    path('upload/', UploadView.as_view(), name='files-upload'),
]
