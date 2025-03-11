from rest_framework import viewsets
from authapp.models import Country
from authapp.serializers import CountrySerializer

class CountryViewSet(viewsets.ModelViewSet):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
