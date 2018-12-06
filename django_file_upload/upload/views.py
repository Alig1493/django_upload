from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views.generic import FormView, ListView

from .models import FileDownload, File
from .forms import FileForm


class UploadView(LoginRequiredMixin, FormView):

    form_class = FileForm
    template_name = "upload/file_upload_script.jinja2"
    login_url = 'auth:login'

    def get_success_url(self):
        return reverse('files:files-list')

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'File uploaded!', fail_silently=True)
        return super().form_valid(form)


class FileListView(LoginRequiredMixin, ListView):

    model = File
    queryset = File.objects.order_by('-id')
    context_object_name = "files"
    template_name = "upload/file_list.jinja2"
    login_url = 'auth:login'
