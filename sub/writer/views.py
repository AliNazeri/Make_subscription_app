from django.shortcuts import render
from django.http import Http404
from django.utils.translation import gettext
from django.views.generic import TemplateView, CreateView, ListView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .forms import article_form
from .models import articles
from account.models import CustomUser

class writer_profile_view(LoginRequiredMixin, TemplateView):
    template_name = 'writer/writer_profile.html'
    login_url = 'login'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        context['name'] = request.user.first_name
        return self.render_to_response(context)
    
class create_article(LoginRequiredMixin, CreateView):
    model = articles
    template_name = 'writer/add_article.html'
    form_class = article_form
    success_url = '/writer/your-articles/'

    def form_valid(self, form):
        form.instance.user = self.request.user
        self.object = form.save()
        return super().form_valid(form)

class read_articles(LoginRequiredMixin, ListView):
    template_name = 'writer/show_articles.html'
    allow_empty = True
    
    def get_queryset(self):
        queryset = articles.objects.filter(user = self.request.user)
        return queryset
    
class editing_articles(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    template_name = 'writer/edit_article.html'
    success_url = '/writer/your-articles/'
    model = articles
    fields = ['title', 'text','is_premium']

    def test_func(self):
        return self.get_object().user == self.request.user

class delete_articles(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    template_name = 'writer/delete_article.html'
    success_url = '/writer/your-articles/'
    model = articles

    def test_func(self):
        return self.get_object().user == self.request.user

class update_profiles(LoginRequiredMixin, UpdateView):
    template_name = 'writer/edit_profile.html'
    success_url = '/writer/writer-profile/'
    model = CustomUser
    fields = ['first_name','last_name']

    def get_object(self):
        return self.request.user
    
class delete_writer(LoginRequiredMixin, DeleteView):
    template_name = 'writer/delete_account_writer.html'
    success_url = ''
    model = CustomUser

    def get_object(self):
        return self.request.user