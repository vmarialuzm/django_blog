from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import redirect
from django.views.generic import CreateView
from .forms import SignUpForm
from django.contrib import messages

class RegisterView(CreateView):
    template_name = "users/signup.html"
    form_class = SignUpForm

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'El registro se ha creado con éxito')
        return redirect('login')
    
    def form_invalid(self, form):
        messages.error(self.request, 'Por favor, completa todos los campos requeridos')
        return super().form_invalid(form)
