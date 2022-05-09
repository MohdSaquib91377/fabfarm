import email
from rest_framework.views import APIView
from rest_framework.response import Response

from .serializers import CustomUserSerializer
from account.models import CustomUser
class RegisterApiView(APIView):
    def post(self,request, *args, **kwargs):
        serializer = CustomUserSerializer(data = request.data)
        if serializer.is_valid():
            
            email_or_mobile = serializer.data['email_or_mobile']
            user = CustomUser.objects.filter(email_or_mobile=email_or_mobile).exists()
            if user:
                return Response({f"status":400,"message":"User already registered with this{email_or_mobile}"})
            
            elif '@' in email_or_mobile:
                return Response(
                    {
                        "status": "200",
                        "message": f"otp sent to {email_or_mobile} successfully",
                    }
                )
                # send otp to mail for verification
            else:
                return Response(
                    {
                        "status": "200",
                        "message": f"otp sent to {email_or_mobile} successfully",
                    }
                )
                # send otp to mobile for verification
        return Response(serializer.errors)

    