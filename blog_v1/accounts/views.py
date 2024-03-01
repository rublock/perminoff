from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import generic

from accounts.forms import SignUpForm, UpdateProfileForm, UpdateUserForm
from blog.forms import LoginForm


class SignUpView(generic.CreateView):
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
    def profile(request):
        if request.method == "POST":
            user_form = UpdateUserForm(request.POST, instance=request.user)
            profile_form = UpdateProfileForm(
                request.POST, request.FILES, instance=request.user.profile
            )

            if user_form.is_valid() and profile_form.is_valid():
                user_form.save()
                profile_form.save()
                messages.success(
                    request, "Your profile is updated successfully"
                )
                return redirect(to="users-profile")
        else:
            user_form = UpdateUserForm(instance=request.user)
            profile_form = UpdateProfileForm(instance=request.user.profile)

        return render(
            request,
            "registration/profile.html",
            {"user_form": user_form, "profile_form": profile_form},
        )
