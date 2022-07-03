import os
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import  csrf_exempt
import requests
# from twilio.twiml.messaging_response import MessagingResponse
from twilio.twiml.messaging_response import Body, Media, Message, MessagingResponse
from twilio.rest import Client

from decouple import config


# Create your views here.


@csrf_exempt
def whatsapp_message_bot(request):
    resp =request.POST
    print (resp)
    response = MessagingResponse()
    response.message('Thank for your message! A member of our team will be '
                     'in touch with you soon.')
    
    return (str(response))
    


@csrf_exempt
def whatsapp_message_image(request):
    user = request.POST.get('From')
    message = request.POST.get('Body')
    media_url = request.POST.get('MediaUrl0')
    phone = user.split(':')[1]  # remove the whatsapp: prefix from the number
    print(f'{user} sent {message}')
    print('Full data',request.POST)

    if media_url:
        r = requests.get(media_url)
        content_type = r.headers['Content-Type']
        
        if content_type == 'image/jpeg':
            filename = f'uploads/{phone}/{message}.jpg'
        elif content_type == 'image/png':
            filename = f'uploads/{phone}/{message}.png'
        elif content_type == 'image/gif':
            filename = f'uploads/{phone}/{message}.gif'
        else:
            filename = None
        if filename:
            if not os.path.exists(f'uploads/{phone}'):
                os.mkdir(f'uploads/{phone}')
            with open(filename, 'wb') as f:
                f.write(r.content)
            msg = 'File Save successfully'
    else:
        msg = 'Just Text'
    resp = MessagingResponse()
    # reply = resp.message()
    # reply.body(msg)
    message = Message()
    message.body(msg)
    resp.append(message)
    send_whatsapp_msg(msg,phone)
    print(resp)
    return HttpResponse(str(resp))


def send_whatsapp_msg(body,phone):

    # Find your Account SID and Auth Token at twilio.com/console
    # and set the environment variables. See http://twil.io/secure
    account_sid = config('TWILIO_ACCOUNT_SID')
    auth_token = config('TWILIO_AUTH_TOKEN')
    client = Client(account_sid, auth_token)

    message = client.messages.create(
                                from_='whatsapp:+14155238886',
                                body=body,
                                to=f'whatsapp:{phone}'
                            )

    print(message.sid)
    
    

@csrf_exempt
def whatsapp_message_status(request):
    print('Full data',request.POST)
    return HttpResponse('Thanks')
    
    
