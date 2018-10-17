from django.contrib.auth import views as auth_views
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models.functions import datetime
from django.utils.functional import cached_property
from django.views.generic.edit import ProcessFormView

from django_file_upload.core.config import UnitType, Session
from django_file_upload.users.utils import (get_unit_models, get_models)
from .forms import CustomAuthForm, YearForm
from django.views.generic import TemplateView


class AuthLoginView(auth_views.LoginView):

    def __init__(self):
        super().__init__()

    template_name = 'users/login.jinja2'
    authentication_form = CustomAuthForm
    redirect_authenticated_user = True


class AuthLogoutView(auth_views.LogoutView):

    def __init__(self):
        super().__init__()

    next_page = 'auth:login'


class BaseView(LoginRequiredMixin, TemplateView):
    login_url = 'auth:login'
    template_name = "users/base.jinja2"


class DashboardView(LoginRequiredMixin, TemplateView, ProcessFormView):
    template_name = "users/sample.jinja2"

    @cached_property
    def get_current_date(self):
        return datetime.datetime.now()

    def get_current_year(self, **kwargs):
        year = kwargs.get("year")
        if year:
            return year
        return self.get_current_date.year

    def get_form(self, **kwargs):
        return YearForm(initial={'year': self.get_current_year(**kwargs)})

    def get_session_list(self, **kwargs):
        year = self.get_current_year(**kwargs)
        months = self.get_current_date.month
        if int(year) > self.get_current_date.year:
            months = 0
        elif int(year) < self.get_current_date.year:
            months = 12
        session_list = []
        for month in range(1, months+1):
            session_list.append(month)
            if month % 3 == 0:
                session_list.append(12+int(month/3))
            if month % 6 == 0:
                session_list.append(16+int(month/6))
        return session_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = self.get_form(**kwargs)
        context["units"] = UnitType.CHOICES
        context["models"] = get_models()
        session_list = self.get_session_list(**kwargs)
        context["sessions"] = session_list
        # Session.get_session_list(limit=self.get_session(year))
        context["unit_models"] = get_unit_models(session__in=session_list, year=self.get_current_year(**kwargs))
        return context

    def post(self, request, *args, **kwargs):
        form = YearForm(request.POST)
        if form.is_valid():
            return self.render_to_response(self.get_context_data(year=form.cleaned_data.get("year")))
        return self.render_to_response(self.get_context_data(year=self.get_current_date.year))
