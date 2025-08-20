
from django.contrib.auth.views import (
	LoginView, LogoutView, PasswordChangeView,
	PasswordResetView, PasswordResetDoneView,
	PasswordResetConfirmView, PasswordResetCompleteView
)
from django.views.generic import CreateView, DetailView, UpdateView
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from .forms import (
	UserLoginForm, UserRegistrationForm, UserProfileUpdateForm,
	UserPasswordChangeForm, CustomPasswordResetForm, CustomSetPasswordForm
)
from django.contrib.auth.models import User
from .models import UserProfile

class UserRegisterView(CreateView):
	model = User
	form_class = UserRegistrationForm
	template_name = 'users/register.html'
	success_url = reverse_lazy('index')
	def dispatch(self, request, *args, **kwargs):
		if request.user.is_authenticated:
			return redirect('index')
		return super().dispatch(request, *args, **kwargs)
	def form_valid(self, form):
		response = super().form_valid(form)
		login(self.request, self.object)
		messages.success(self.request, 'Registration successful!')
		return response

class UserLoginView(LoginView):
	form_class = UserLoginForm
	template_name = 'users/login.html'
	redirect_authenticated_user = True
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['title'] = 'Login'
		context['button_text'] = 'Log in'
		return context
	def form_valid(self, form):
		messages.success(self.request, 'Login successful!')
		return super().form_valid(form)

class UserLogoutView(LogoutView):
	next_page = reverse_lazy('index')
	def dispatch(self, request, *args, **kwargs):
		messages.success(request, 'Logged out successfully!')
		return super().dispatch(request, *args, **kwargs)

class UserProfileDetailView(LoginRequiredMixin, DetailView):
	model = User
	template_name = 'users/profile_detail.html'
	context_object_name = 'user_obj'
	def get_object(self, queryset=None):
		obj = super().get_object(queryset)
		if obj != self.request.user:
			return self.request.user
		return obj

class UserProfileUpdateView(LoginRequiredMixin, UpdateView):
	model = UserProfile
	form_class = UserProfileUpdateForm
	template_name = 'users/profile_update_form.html'
	success_url = reverse_lazy('profile_detail')
	def get_object(self, queryset=None):
		return self.request.user.profile
	def form_valid(self, form):
		messages.success(self.request, 'Profile updated successfully!')
		return super().form_valid(form)

class UserPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
	form_class = UserPasswordChangeForm
	template_name = 'users/password_change_form.html'
	success_url = reverse_lazy('profile_detail')
	def form_valid(self, form):
		messages.success(self.request, 'Password changed successfully!')
		return super().form_valid(form)

class CustomPasswordResetView(PasswordResetView):
	form_class = CustomPasswordResetForm
	template_name = 'users/password_reset_form.html'
	email_template_name = 'users/password_reset_email.html'
	success_url = reverse_lazy('password_reset_done')

class CustomPasswordResetDoneView(PasswordResetDoneView):
	template_name = 'users/password_reset_done.html'

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
	form_class = CustomSetPasswordForm
	template_name = 'users/password_reset_confirm.html'
	success_url = reverse_lazy('password_reset_complete')

class CustomPasswordResetCompleteView(PasswordResetCompleteView):
	template_name = 'users/password_reset_complete.html'

# Create your views here.
