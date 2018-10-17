from django.conf.urls import url

from django_file_upload.users.views import AuthLoginView, AuthLogoutView, DashboardView

app_name = "users"

urlpatterns = [
    url('^$', AuthLoginView.as_view(), name='login'),
    url('^logout/$', AuthLogoutView.as_view(), name='logout'),
    # url('^base/$', BaseView.as_view(), name='base'),
    url('^dashboard/$', DashboardView.as_view(), name='dashboard'),
]
