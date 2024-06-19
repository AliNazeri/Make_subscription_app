from typing import Any
from django.shortcuts import render, redirect, HttpResponse
from django.urls import reverse_lazy
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LogoutView
from django.contrib.auth import authenticate, login, logout
from django.views.generic import TemplateView, CreateView
from .forms import user_reg_form
from .models import CustomUser
from django.views import View
from django.conf.global_settings import EMAIL_HOST_USER

from .token import user_tokenizer_generate
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.core.mail import send_mail

class home_view(TemplateView):
    template_name = 'account/index.html'
  
class register_view(CreateView):
    model = CustomUser
    form_class = user_reg_form
    template_name = 'account/register.html'
    success_url = '/login/' # if email is connected change to '/email-verification-sent'

    def form_valid(self, form):
        self.object = form.save()

        # Uncomment after add email
        
        # current_site = get_current_site(self.request)
        # message = render_to_string('account/email-verification.html',{
        #     'user': self.object,
        #     'domain': current_site.domain,
        #     'uid': urlsafe_base64_encode(force_bytes(self.object.pk)),
        #     'token': user_tokenizer_generate.make_token(self.object)
        # })
        # send_mail(subject='Ativate your account', message=message, from_email=EMAIL_HOST_USER, recipient_list=[self.object.email])

        return super().form_valid(form)

        
    
class login_view(TemplateView):
    template_name = 'account/login.html'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['form'] = AuthenticationForm()
        return context
    
    def post(self, request):
        userform = AuthenticationForm(request, request.POST)
        if userform.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username = username, password = password)
            if user.is_active:
                if user and user.is_writer:
                    login(request,user)

                    return redirect('writer-profile')
                
                if user and not user.is_writer:
                    login(request,user)

                    return redirect('client-profile')
            else:
                return redirect('email-verification-sent')
            
        return render(request, template_name='account/login.html', context = {'form':userform})

class logout_view(LogoutView):
    next_page = 'login'

class email_verification_failed(TemplateView):
    template_name = 'account/email_verification_failed.html'

class email_verification_success(TemplateView):
    template_name = 'account/email_verification_success.html'

class email_verification_sent(TemplateView):
    template_name = 'account/email_verification_sent.html'

class email_verification(View):
    def get(self, request, uidb64, token):

        unique_token = force_str(urlsafe_base64_decode(uidb64))

        try:
            user = CustomUser.objects.get(pk=unique_token)
            if user_tokenizer_generate.check_token(unique_token, token):
                user.is_active = True
                user.save()
                
                return redirect('email-verification-success')
            else:
                return redirect('email-verification-failed')

        except user.DoesNotExist:
            return HttpResponse("Your user account is not created")