from rest_framework import generics
from banner.models import *
from .serializers import BannerSerializer
# Banner Api
class BannerAPIView(generics.ListAPIView):
    queryset = Banner.objects.all()
    serializer_class = BannerSerializer

    def get_queryset(self):
        page_name = self.kwargs['page_name']
        queryset = Banner.objects.filter(page__icontains = page_name)
        return queryset