from django.shortcuts import render
import json
from .models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate 
from rest_framework_simplejwt.tokens import RefreshToken
import random
from django.core.cache import cache
from django.conf import settings
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives

# Create your views here.
@csrf_exempt
def userRegistration(request):
    try:
        if request.method!= "POST":
            raise Exception("Method not allowed")
        else:
            data = json.loads(request.body)
            email = data['email']
            fName =  data['first_name']
            lName =  data['last_name']
            usernamee =  data['username']
            passwordd =  data['password']

            user = User.objects.create_user(email = email, password = passwordd, username = usernamee, first_name = fName, last_name = lName)

            return JsonResponse({
                "status":"Success",
                "message": f"User {fName} {lName} with emai {email} registered successfully"
            })

    except Exception as ex:
        return JsonResponse({
            "status":"Failed",
            "message":str(ex)
        })
    
@csrf_exempt
def login(request):
    try:
        if request.method!= "POST":
            raise Exception("Method not allowed")
        else:
            data = json.loads(request.body)

            usernamee =  data['username']
            passwordd =  data['password']

            userObj = User.objects.filter(username = usernamee).exists()

            if userObj == True:
                user = authenticate(request, username = usernamee, password = passwordd)

                if user is not None:
                    refresh = RefreshToken.for_user(user)

                    return JsonResponse({
                        "status":"success",
                        "message":"login successful",
                        "refreshToken":str(refresh),
                        "accessToken":str(refresh.access_token)
                    })
            
    except Exception as ex:
        return JsonResponse({
            "status":"Failed",
            "message":str(ex)
        })

@csrf_exempt
def sendOtp(request):
    try:
        if request.method!= "POST":
            raise Exception("Method not allowed")
        
        else:
            email=(json.loads(request.body))["email"]

            userObj = User.objects.filter(email = email).exists()

            if userObj==False:
                return JsonResponse({
                "status":"Failed",
                "message": "User not registered"
                })
            else:
                otp=random.randint(1000,9999)
                cache.set(email, otp , timeout=600)

                subject = "otp for reset password"
                from_email = settings.EMAIL_HOST_USER
                to_email =[email]

                html_message=render_to_string("send_otp.html",{"otp":otp})
                email= EmailMultiAlternatives(subject,'',from_email,to_email)
                email.attach_alternative(html_message,'text/html')
                email.send()
                return JsonResponse({
                        "status":"success",
                        "message":"OTP sent successfully"
                    })



    except Exception as ex:
        return JsonResponse({
            "status":"Failed",
            "message":str(ex)
        })

