from django.conf.global_settings import MEDIA_ROOT
from django.contrib import messages
from django.shortcuts import render
from django.views.static import serve
from django.urls import reverse
from django.views.generic import TemplateView, FormView, ListView

from upload.forms import FileForm
from upload.models import File


class UploadView(FormView):

    form_class = FileForm
    template_name = "upload/file_upload_script.jinja2"

    def get_success_url(self):
        return reverse('files:files-list')

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'File uploaded!', fail_silently=True)
        return super().form_valid(form)


class FileListView(ListView):

    model = File
    queryset = File.objects.order_by('-id')
    context_object_name = "files"
    template_name = "upload/file_list.jinja2"
