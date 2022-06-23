from rest_framework import generics
from banner.models import *
from .serializers import PageSerializer
# Banner Api
class PageAPIView(generics.ListAPIView):
    queryset = Page.objects.all()
    serializer_class = PageSerializer

    def get_queryset(self):
        page_name = self.kwargs['page_name']
        queryset = Page.objects.filter(page__icontains = page_name)
        return queryset