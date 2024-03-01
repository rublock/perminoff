from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import View, generic

from accounts.forms import (
    ChangePasswordForm,
    SignUpForm,
    UpdateProfileForm,
    UpdateUserForm,
)
from blog.forms import LoginForm


class SignUpView(generic.CreateView):
    """Отображение регистрации пользователя"""

    form_class = SignUpForm
    success_url = reverse_lazy("login")
    initial = None
    template_name = "registration/signup.html"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(to="/")

        return super(SignUpView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {"form": form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            form.save()

            username = form.cleaned_data.get("username")
            messages.success(request, f"Account created for {username}")

            return redirect(to="login")

        return render(request, self.template_name, {"form": form})


class CustomLoginView(LoginView):
    """Переопределение стандартного LoginView установка сессий"""

    form_class = LoginForm

    def form_valid(self, form):
        remember_me = form.cleaned_data.get("remember_me")

        if not remember_me:
            self.request.session.set_expiry(0)
            self.request.session.modified = True

        return super(CustomLoginView, self).form_valid(form)


@login_required
def profile(request):
    """Отображение редактирования профиля"""
    if request.method == "POST":
        user_form = UpdateUserForm(request.POST, instance=request.user)
        profile_form = UpdateProfileForm(
            request.POST, request.FILES, instance=request.user.profile
        )

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Your profile is updated successfully")
            return redirect(to="accounts:users-profile")
    else:
        user_form = UpdateUserForm(instance=request.user)
        profile_form = UpdateProfileForm(instance=request.user.profile)

    return render(
        request,
        "registration/profile.html",
        {"user_form": user_form, "profile_form": profile_form},
    )


class ChangePasswordView(View):
    """Отображение изменения пароля"""

    template_name = "registration/change_password.html"

    def get(self, request, *args, **kwargs):
        form = ChangePasswordForm(
            request.user
        )  # Передаем пользователя как аргумент при инициализации формы
        return render(request, self.template_name, {"form": form})

    def post(self, request, *args, **kwargs):
        form = ChangePasswordForm(
            request.user, request.POST
        )  # Передаем пользователя и данные POST при инициализации формы
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(
                request, user
            )  # Важно для сохранения сессии пользователя
            messages.success(
                request, ("Your password was successfully updated!")
            )
            return redirect("accounts:users-profile ")
        else:
            messages.error(request, ("Please correct the error below."))
            return render(request, self.template_name, {"form": form})
