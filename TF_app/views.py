from django.shortcuts import render,redirect
from django.http import HttpResponse,HttpResponseRedirect
from TF_app.form import login,register
from django.core.mail import EmailMessage
from django.template.loader import render_to_string,get_template
from django.contrib.auth.models import User
from background_task import background
from django.utils.encoding import force_text,force_bytes
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.contrib.auth import authenticate,login as Login,logout
from django.contrib.auth.decorators import login_required
import hashlib
import time


# Create your views here.

def index_view(request):
    return render(request,'index.html',{'Name':'Mohit Suthar'})

def login_view(request):
    form=login()
    if request.method == 'POST':
        form=login(request.POST)
        if form.is_valid():
            username=form.cleaned_data['username']
            password=form.cleaned_data['password']
            user = authenticate(username=username,password=password)
            if user is not None:
                if user.is_active:
                    login(request,user)
                    return HttpResponse('login successfull')
                else:
                    return HttpResponse('account disabled')
            else:
                return HttpResponse('username or password invalid')
    return render(request,'login.html',{'login_form':form})




def register_view(request):
    form=register()
    if request.method == 'POST':
        form=register(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            user =User.objects.create_user(
                username=username,
                password=form.cleaned_data['password'],
                email=email,
            )
            user.is_active=False
            user.is_superuser=False
            user.is_staff=False
            user.save()
            user_data=User.objects.get(username=form.cleaned_data['username'])
            token_data=str(user_data.date_joined)+username+email+str(user_data.pk)
            token = hashlib.sha1(token_data.encode()).hexdigest()
            uid = urlsafe_base64_encode(force_bytes(user_data.pk))
            send_mail(username,email,token,uid)
            request.session['link_send_email']=email
            delete_user(user_data.pk)
            return redirect('link_send')
    return render(request,'register.html',{'register_form':form})

@background(schedule=60)
def delete_user(user_id):
    user=User.objects.get(pk=user_id)
    if not user.is_active:
        user.delete()

def send_mail(username,email,token,uid):
    try:
        message =get_template('active_account.html').render({
            'username':username,
            'token':token,
            'uid':uid})
        msg = EmailMessage(
        'Acriveation Key for Team Firecode account',
        message,
        'teamfirecode.project@gmail.com',
        [email],
        )
        msg.content_subtype='html'
        msg.send()
    except:
        return HttpResponse('plz try again')

        


def link_active_view(request,uid,token):
    try:
        uid_user=urlsafe_base64_decode(force_text(uid))
        user=User.objects.get(id=uid_user)
        token_data=str(user.date_joined)+user.username+user.email+str(user.pk)
        main_token = hashlib.sha1(token_data.encode()).hexdigest()
        if not user.is_active:
            if token == main_token:
                user.is_active=True
                user.save()
                return HttpResponse('active')
        else:
            return HttpResponse('active already')
    except:
        return HttpResponse('invalid link')
def link_send_view(request):
    try:
        link_email=request.session['link_send_email']
        if link_email:
            del request.session['link_send_email']
            return render(request,'link_send.html',{'email':link_email})
    except:
        return redirect('login')
