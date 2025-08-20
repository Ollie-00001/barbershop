
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.contrib import messages
from .forms import UserLoginForm, UserRegistrationForm
from django.contrib.auth.models import User

class UserLoginView(LoginView):
	form_class = UserLoginForm
	template_name = 'users/form.html'
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['title'] = 'Login'
		context['button_text'] = 'Log in'
		return context

class UserRegistrationView(CreateView):
	model = User
	form_class = UserRegistrationForm
	template_name = 'users/form.html'
	success_url = reverse_lazy('login')
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['title'] = 'Register'
		context['button_text'] = 'Sign up'
		return context
	def form_valid(self, form):
		messages.success(self.request, 'Регистрация прошла успешно! Теперь вы можете войти в свой аккаунт.')
		return super().form_valid(form)

class UserLogoutView(LogoutView):
	next_page = reverse_lazy('index')

# Create your views here.
