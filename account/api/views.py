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
from django.http import Http404
from drf_yasg.utils import swagger_auto_schema

class RegisterApiView(APIView):
    @swagger_auto_schema(tags = ['account'],request_body = RegisterSerializer)
    def post(self,request, *args, **kwargs):
        try:
            serializer = RegisterSerializer(data = request.data)
            if serializer.is_valid():
                email_or_mobile = request.data.get('email_or_mobile')
                user = CustomUser.objects.filter(email_or_mobile=email_or_mobile).first()
                if user and not user.is_verified:
                    user.delete()
                elif user and user.is_verified:
                    return Response({"status":"400","message":f"{email_or_mobile} already exists plz login"},status= status.HTTP_400_BAD_REQUEST)
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
    @swagger_auto_schema(tags = ['account'],request_body = OTPVerifySerializer)
    def post(self,request,*args, **kwargs):
        try:
            serializer = OTPVerifySerializer(data = request.data)
            if serializer.is_valid():
                user = CustomUser.objects.filter(id = serializer.data['id'],otp = serializer.data['otp']).first()
                if user:
                    if not user.is_expired:
                        CustomUser.objects.filter(id = serializer.data['id'],otp = serializer.data['otp']).update(is_verified=True)
                        # Generrate Token
                        token = get_tokens_for_user(user)
                        return Response({"status":"200","message":"OTP verify successfully","data":token})
                    else:
                        return Response({"status":"400","message":"OTP expire"},status= status.HTTP_400_BAD_REQUEST)
                return Response({"status":"400","message":"Invalid OTP"},status= status.HTTP_400_BAD_REQUEST)
            return Response(serializer.errors,status = status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"status":"400","message":f"{e}"},status= status.HTTP_400_BAD_REQUEST)

class SendOTPAPIView(APIView):
    @swagger_auto_schema(tags = ['account'],request_body = SendOTPSerializer)
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
                return Response({"status":"400","message":"Invalid credentials"},status= status.HTTP_400_BAD_REQUEST)    
            return Response(serializer.errors,status = status.HTTP_400_BAD_REQUEST)       
        except Exception as e:
            return Response({"status":"400","message":f"{e}"},status= status.HTTP_400_BAD_REQUEST)

class LoginApiView(APIView):
    
    try:
        def get_object(self,email_or_mobile):
            return CustomUser.objects.filter(email_or_mobile = email_or_mobile).first()
    except CustomUser.DoesNotExist:
        raise Http404
    @swagger_auto_schema(tags = ['account'],request_body = LoginSerializer)
    def post(self, request, *args, **kwargs):
        try:
            serializer = LoginSerializer(data = request.data)
            if serializer.is_valid():
                user = authenticate(self,email_or_mobile=serializer.data["email_or_mobile"],password = serializer.data['password'])
                if user:
                    user.is_verified = True
                    user.save()
                    #Generate Token
                    token = get_tokens_for_user(user)
                    return Response({"status":"200","message":"Login Successfully","data":token})
                return Response({"status":"400","message":"Invalid credentials"},status= status.HTTP_400_BAD_REQUEST)
            return Response(serializer.errors,status = status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({"status":"400","message":f"{e}"},status= status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(tags = ['account'],request_body = LoginSerializer)       
    def put(self, request, *args, **kwargs):
        try:
            instance = self.get_object(request.data.get("email_or_mobile"))
            serializer = LoginSerializer(instance, data=request.data)
            if serializer.is_valid():
                password = make_password(request.data.get("password"))
                serializer.save(password=password)
                return Response({"status":"200","message":"Password update successfully"})
            return Response(serializer.errors,status = status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"status":"400","message":f"{e}"},status= status.HTTP_400_BAD_REQUEST)