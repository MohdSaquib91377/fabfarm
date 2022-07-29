from re import S
from rest_framework.views import APIView
from rest_framework.response import Response
from services.email import send_mail
from services.otp import send_twilio_sms
from .serializers import (ChangePasswordSerializer, RegisterSerializer,OTPVerifySerializer,SendOTPSerializer,
                            LoginSerializer,LogoutSerializer,ListUpdateProfileSerializer,UpdateEmailSerializer,MobileSerializer,UpdateMobileSerializer)
from account.models import CustomUser
from account.helpers import (get_tokens_for_user,verify_otp,send_otp_on_entered_email_or_exists_one,
                            verify_updated_email_or_exists_one,send_otp_on_entered_mobile_or_exists_one,verify_and_update_mobile)
from rest_framework import status
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from django.http import Http404
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
import this
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.views import TokenViewBase
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError


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
    permission_classes = [IsAuthenticated]

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
                if user and user.is_verified:
                    user.is_verified = True
                    user.save()
                    #Generate Token
                    token = get_tokens_for_user(user)
                    user_info = {
                        "fullname": user.fullname,
                        "email_or_mobile": user.email_or_mobile

                    }
                    return Response({"status":"200","message":"Login Successfully","data":token,"user_info":user_info})
                elif user:
                    return Response({"status":"400","message":f"Please verify your {serializer.data['email_or_mobile']}"},status = status.HTTP_403_FORBIDDEN)
                else:
                    return Response({"status":"400","message":"Invalid credentials"},status= status.HTTP_400_BAD_REQUEST)
            return Response(serializer.errors,status = status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({"status":"400","message":f"{e}"},status= status.HTTP_400_BAD_REQUEST)


class LogoutAPIView(generics.GenericAPIView):
    serializer_class = LogoutSerializer
    permission_classes = [IsAuthenticated]

    def post(self,request,*args, **kwargs):
        serializer = self.serializer_class(data = request.data)
        serializer.is_valid(raise_exception = True)
        serializer.save()
        return Response({"status":"200","message":"logout  successfully"},status=status.HTTP_200_OK)
       


class InvalidUser(AuthenticationFailed):
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = ('Credentials is invalid or expired')
    default_code = 'user_credentials_not_valid'

class CustomTokenRefreshView(TokenViewBase):
    """
    Takes a set of user credentials and returns an access and refresh JSON web
    token pair to prove the authentication of those credentials.
    """
    serializer_class = TokenRefreshSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except AuthenticationFailed as e:
            raise InvalidUser(e.args[0])
        except TokenError as e:
            raise InvalidUser(e.args[0])

        return Response(serializer.validated_data, status=status.HTTP_200_OK)


class ChangePasswordAPIView(APIView):
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(tags = ['account'],request_body = ChangePasswordSerializer)       
    def put(self, request, *args, **kwargs):
        serializer = ChangePasswordSerializer(data = request.data)
        serializer.is_valid(raise_exception = True) 

        # verify otp    
        msg,status = verify_otp({"txn_id":serializer.validated_data["txn_id"],"otp":serializer.validated_data["otp"]})   
        if status == 404:
            return Response({"status":"404","message":f"{msg}"},status=404)

        if status == 400:
            return Response({"status":"400","message":f"{msg}"},status=400)

        if not request.user.check_password(serializer.validated_data["current_password"]):
            return Response({"status":"400","message":f"old password is not match"},status=401) 

        if serializer.validated_data["new_password"] != serializer.validated_data["confirm_password"]:
            return Response({"status":"400","message":f"new password or confirm password does not match "},status=400) 
        # make hash password
        request.user.set_password(serializer.validated_data["new_password"])
        request.user.save()
        return Response({"status":"200","message":f"password changed successfully"},status=200) 


class ListUpdateUpdateProfileAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ListUpdateProfileSerializer

    def get(self, request,*args, **kwargs):
        serializer = self.serializer_class(request.user)
        return Response(serializer.data)

    @swagger_auto_schema(tags = ['account'],request_body = ListUpdateProfileSerializer)       
    def patch(self, request, *args, **kwargs):
        serializer = self.serializer_class(request.user,data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

class UpdateEmailAPIView(APIView):
    serializer_class = UpdateEmailSerializer
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(tags = ['account'],request_body = SendOTPSerializer)       
    def post(self, request, *args, **kwargs):
        serializer = SendOTPSerializer(data = request.data)
        serializer.is_valid(raise_exception = True)
        msg,status = send_otp_on_entered_email_or_exists_one({"new_email": serializer.validated_data["email_or_mobile"],"user_id": request.user.id,"exists_email":request.user.email_or_mobile})
        if status == 400:
            return Response({"status":f"{status}","message":f"{msg}"})
            
        return Response({"status":f"{status}","message":f"{msg}"}) 

    @swagger_auto_schema(tags = ['account'],request_body = UpdateEmailSerializer)       
    def patch(self, request, *args, **kwargs):
        serializer = self.serializer_class(data = request.data)
        serializer.is_valid(raise_exception = True)
        data = {
            "new_email_otp":serializer.validated_data["new_email_otp"],
            "exists_email_otp":serializer.validated_data["exists_email_otp"],
            "password":serializer.validated_data["password"],
        }
        msg,status = verify_updated_email_or_exists_one(data)
        if status == 404:
            return Response({"status":"404","message":f"{msg}"},status=404)
        if status == 400:
            return Response({"status":"400","message":f"{msg}"},status=400)

        return Response({"status":f"{status}", "message":f"{msg}"},status=200)

class UpdateMobileAPIView(APIView):
    serializer_class = UpdateMobileSerializer
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(tags = ['account'],request_body = MobileSerializer)       
    def post(self, request, *args, **kwargs):
        serializer = MobileSerializer(data = request.data)
        serializer.is_valid(raise_exception = True)
        msg,status = send_otp_on_entered_mobile_or_exists_one({"new_mobile": serializer.validated_data["mobile"],"user_id": request.user.id,"exists_mobile":request.user.mobile})
        if status == 400:
            return Response({"status":f"{status}","message":f"{msg}"})
            
        return Response({"status":f"{status}","message":f"{msg}"}) 

    @swagger_auto_schema(tags = ['account'],request_body = UpdateMobileSerializer)       
    def patch(self, request, *args, **kwargs):
        serializer = self.serializer_class(data = request.data)  
        serializer.is_valid(raise_exception = True)

        data = {
            "new_mobile_otp":serializer.validated_data["new_mobile_otp"],
            "exists_email_or_mobile_otp":serializer.validated_data["exists_email_or_mobile_otp"],
            "password":serializer.validated_data["password"],
        }
        msg,status = verify_and_update_mobile(data,request.user)

        if status == 400:
            return Response({"status":f"{status}","message":f"{msg}"},status=400)
        
        return Response({"status":f"{status}","message":f"{msg}"},status=status)