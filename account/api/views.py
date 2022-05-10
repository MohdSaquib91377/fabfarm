import email
from rest_framework.views import APIView
from rest_framework.response import Response
from services.email import send_mail
from services.otp import send_twilio_sms
from .serializers import RegisterSerializer,OTPVerifySerializer,SendOTPSerializer,LoginSerializer
from account.models import CustomUser
from account.helpers import get_tokens_for_user
from rest_framework import status
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password

class RegisterApiView(APIView):
    def post(self,request, *args, **kwargs):
        try:
            serializer = RegisterSerializer(data = request.data)
            if serializer.is_valid():
                email_or_mobile = request.data.get('email_or_mobile')
                user = CustomUser.objects.filter(email_or_mobile=email_or_mobile).first()
                if user and not user.is_verified:
                    user.delete()
                elif user and user.is_verified:
                    return Response({"status":"400","message":f"{email_or_mobile} already exists plz login"})
                password = make_password(self.request.data['password'])
                user = serializer.save(password=password)   
                if '@' in email_or_mobile:
                    send_mail('Please verify your otp',f"your otp is {user.otp}",{email_or_mobile})

                    return Response(
                        {
                            "status": "200",
                            "otp": user.otp,
                            "id": user.id
                        }
                    )
                else:
                    send_twilio_sms(email_or_mobile,f"{user.otp}")
                    return Response(
                        {
                            "status": "200",
                            "otp": user.otp,
                            "id": user.id
                        }
                    )
                
            return Response(serializer.errors)
        except Exception as e:
              return Response(
                            {
                                "status": "400",
                                "message": f"{e}",
                            }
                        )
        
class VerifyOTPApiView(APIView):
    def post(self,request,*args, **kwargs):
        try:
            serializer = OTPVerifySerializer(data = request.data)
            if serializer.is_valid():
                user = CustomUser.objects.filter(id = serializer.data['id'],otp = serializer.data['otp']).first()
                if user:
                    if not user.is_expired:
                        CustomUser.objects.filter(id = serializer.data['id'],otp = serializer.data['otp']).update(is_verified=True)
                        return Response({"status":"200","message":"OTP verify successfully"})
                    else:
                        return Response({"status":"400","message":"OTP expire"})
                return Response({"status":"400","message":"Invalid OTP"})
            return Response(serializer.errors,status = status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"status":"400","message":f"{e}"})

class SendOTPAPIView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            serializer = SendOTPSerializer(data = request.data)
            if serializer.is_valid():
                user = CustomUser.objects.filter(email_or_mobile = serializer.data["email_or_mobile"]).first()
                if user:
                    user = CustomUser.objects.get(email_or_mobile = serializer.data["email_or_mobile"])
                    user.save()
                    if '@' in serializer.data["email_or_mobile"]:
                        send_mail('Please verify your otp',f"your otp is {user.otp}",{serializer.data["email_or_mobile"]})

                        return Response(
                            {
                                "status": "200",
                                "otp": user.otp,
                                "id": user.id
                            }
                        )
                    else:
                        send_twilio_sms(serializer.data["email_or_mobile"],f"{user.otp}")
                        return Response(
                            {
                                "status": "200",
                                "otp": user.otp,
                                "id": user.id
                            }
                        )
                return Response({"status":"400","message":"Invalid credentials"})    
            return Response(serializer.errors,status = status.HTTP_400_BAD_REQUEST)       
        except Exception as e:
            return Response({"status":"400","message":f"{e}"})

class LoginApiView(APIView):
    def post(self, request, *args, **kwargs):
        try:

            serializer = LoginSerializer(data = request.data)
            if serializer.is_valid():
                user = authenticate(self,email_or_mobile=serializer.data["email_or_mobile"],password = serializer.data['password'])
                if user:
                    user.is_verified = True
                    user.save()
                    return Response({"status":"200","message":"Login Successfully"})
                return Response({"status":"400","message":"Invalid credentials"})
            return Response(serializer.errors,status = status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({"status":"400","message":f"{e}"})
