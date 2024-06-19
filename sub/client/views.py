from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render, redirect, HttpResponse
from django.views.generic import TemplateView, ListView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import subscription
from account.models import CustomUser
from .forms import client_profile_form
from writer.models import articles
from .paypal import get_access_token, cancel_subscription, update_sub_paypal, get_current_subscription

class client_profile_view(LoginRequiredMixin, TemplateView):
    template_name = 'client/client_profile.html'
    login_url = 'login'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['name'] = self.request.user.first_name
        try:
            user_sub = subscription.objects.get(subscriber_user=self.request.user, is_active=True)
            context['subscription'] = user_sub.subscription_plan
        except:
            context['subscription'] = None

        return context
    
class client_articles_view(ListView):
    template_name = 'client/show_articles.html'
    model = subscription

    def get_queryset(self) -> QuerySet[Any]:
        qs = super().get_queryset()

        try:
            result = qs.get(subscriber_user=self.request.user, is_active=True)
        except:
            return None
        
        if result.subscription_plan == 'P':
            return articles.objects.all()
        if result.subscription_plan == 'S':
            return articles.objects.filter(is_premium = False)


class create_subscription(LoginRequiredMixin, TemplateView):
    template_name = 'client/successfuly_subscribed.html'

    def get(self, request, subID, plan):

        sub_cost = ''
        if plan == 'Standard':
            sub_cost = '4.99'

        elif plan == 'Premium':
            sub_cost = '9.99'

        created_sub = subscription.objects.create(
            subscriber_name = request.user.first_name + ' ' + request.user.last_name,
            subscription_plan = plan[0],
            subscription_cost = sub_cost,
            paypal_susbscription_id = subID,
            is_active = True,
            subscriber_user = request.user
            )
        
        return super(TemplateView, self).render_to_response({'subscription':created_sub})

class account_management(LoginRequiredMixin, TemplateView):
    template_name = 'client/account_management.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        form = client_profile_form(instance=request.user)
        context['form'] = form
        try:
            subscription.objects.get(subscriber_user=request.user, is_active = True)
            context['subscribed'] = True

        except:
            self.user_subid = None
            context['subscribed'] = False

        return self.render_to_response(context)
    
    def post(self, request,*args, **kwargs):
        if 'edit-profile' in request.POST:
            edited_form = client_profile_form(request.POST, instance=request.user)
            if edited_form.is_valid():
                edited_form.save()

            else:

                context = self.get_context_data(**kwargs)
                context['form'] = edited_form
                return self.render_to_response(context)
                

        elif 'cancel-sub' in request.POST:
            subID = subscription.objects.get(subscriber_user=self.request.user, is_active = True).paypal_susbscription_id

            access_token = get_access_token()
            cancel_subscription(access_token, subID)

            user_sub = subscription.objects.get(subscriber_user=self.request.user, paypal_susbscription_id = subID)

            user_sub.delete()

        return redirect("client-profile")


class update_paypal_subscription(LoginRequiredMixin, TemplateView):
    template_name = 'client/confirm_paypal_update.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        try: 
            user_subid = subscription.objects.get(subscriber_user=request.user, is_active = True).paypal_susbscription_id

            token = get_access_token()
            link = update_sub_paypal(token, user_subid)
            
            if link:
                context['paypal_accepted'] = True
                return redirect(link)
        except:
            return redirect("client-profile")
        
        return self.render_to_response(context)
    
class update_sub_success(TemplateView):
    template_name = 'client/success_update_paypal_sub.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)

        token = get_access_token()
        user_subid = subscription.objects.get(subscriber_user=self.request.user, is_active = True).paypal_susbscription_id
        try:
            current_plan_id = get_current_subscription(token,user_subid)

            if current_plan_id == '': # this is standard plan id
                new_plan_name = 'S'
                new_cost = '4.99'

            elif current_plan_id == '': # this is premium plan id
                new_plan_name = 'P'
                new_cost = '9.99'

            try:
                sub = subscription.objects.get(paypal_susbscription_id=user_subid)
                sub.subscription_cost = new_cost
                sub.subscription_plan = new_plan_name
                sub.save()
                return self.render_to_response(context)

            except subscription.DoesNotExist:
                print('subscription object for updating is not found')
                return HttpResponse('Something went wrong try again later')
        except:
            return HttpResponse('Something went wrong try again later (paypal request failed)')

class delete_client(LoginRequiredMixin, DeleteView):
    template_name = 'client/delete_account_client.html'
    success_url = ''
    model = CustomUser

    def get_object(self):
        return self.request.user
    
