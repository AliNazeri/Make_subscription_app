import requests
import json
from .models import subscription

def get_access_token():

    data = {'grant_type':'client_credentials'}

    headers = {'Accept':'application/json','Accept-Language':'en_US'}

    client_id = '' # client id of paypal business account

    secret_id = '' # secrect id of paypal business account

    url = 'https://api.sandbox.paypal.com/v1/oauth2/token'

    req = requests.post(url, auth=(client_id,secret_id), headers=headers, data=data).json()

    access_token = req['access_token']

    return access_token

def cancel_subscription(access_token, subId):
    bearer_token = 'Bearer '+ access_token

    headers = {'Content-Type' : 'application/json',
               'Authorization' : bearer_token,}
    
    url = 'https://api.sandbox.paypal.com/v1/billing/subscriptions/' + subId + '/cancel'
    
    req = requests.post(url, headers=headers)

    print(req.status_code)


def update_sub_paypal(access_token, subId):
    bearer_token = 'Bearer '+ access_token

    headers = {'Content-Type' : 'application/json',
               'Authorization' : bearer_token,}

    url = 'https://api.sandbox.paypal.com/v1/billing/subscriptions/' + subId + '/revise'

    sub_plan = subscription.objects.get(paypal_susbscription_id = subId).subscription_plan

    if sub_plan == 'P':
        new_plan_id = '' # this is standard plan id
    elif sub_plan == 'S':
        new_plan_id = '' # this is premium plan id
    
    data = {
        'plan_id': new_plan_id
    }

    req = requests.post(url, headers=headers, data=json.dumps(data))

    response_data = req.json()

    approve_link = None
    for link in response_data.get('links',[]):
        if link.get('rel') == 'approve':
            approve_link = link['href']
            break
    
    if req.status_code == 200:
        print('request success')

        return approve_link
    else:
        print('failed request')

def get_current_subscription(access_token, subId):
    bearer_token = 'Bearer '+ access_token

    headers = {'Content-Type' : 'application/json',
               'Authorization' : bearer_token,}
    
    url = 'https://api.sandbox.paypal.com/v1/billing/subscriptions/' + subId

    req = requests.get(url,headers=headers)

    if req.status_code == 200:
        subscription_data = req.json().get('plan_id')
        print(subscription_data)
        return subscription_data
    else:
        print('request failed', req.status_code)

        return None
