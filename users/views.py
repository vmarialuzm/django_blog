from django.shortcuts import redirect
from django.views.generic import CreateView
from django.contrib.auth.forms import UserCreationForm

class RegisterView(CreateView):
    template_name = "users/signup.html"
    form_class = UserCreationForm

    def form_valid(self, form):
        form.save()
        return redirect('login')
