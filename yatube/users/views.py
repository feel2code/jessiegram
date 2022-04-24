from django.http import HttpResponseRedirect
from django.views.generic import CreateView
from django.contrib.auth import authenticate, login
from django.urls import reverse, reverse_lazy

from .forms import CreationForm


class SignUp(CreateView):
    form_class = CreationForm
    success_url = reverse_lazy('posts:index')
    template_name = 'users/signup.html'

    # auto login after register:
    def form_valid(self, form):
        # save the new user first
        form.save()
        # get the username and password
        # username =
        self.request.POST['username']
        # password =
        self.request.POST['password1']
        # authenticate user then login
        user = authenticate(
            username=form.cleaned_data['username'],
            password=form.cleaned_data['password1'],
        )
        login(self.request, user)
        return HttpResponseRedirect(reverse('posts:index'))
