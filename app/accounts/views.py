from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView

from .forms.signup import SignUpForm    

@login_required
def profile(request):
    return render(request, template_name='accounts/profile.html')

class SignUpView(CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy("profile")
    template_name = "accounts/signup.html"

    def form_valid(self, form):
        user = form.save()

        # アップロードされたアイコンがある場合、ユーザーのアイコンとして保存
        if "profile_icon" in self.request.FILES:
            user.profile_icon = self.request.FILES["profile_icon"] 
            print(user.profile_icon)
        user.save()
        login(self.request, user)
        self.object = user
        return redirect(self.get_success_url())
    