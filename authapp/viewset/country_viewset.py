from rest_framework import viewsets
from authapp.models import Country
from authapp.serializers import CountrySerializer

class CountryViewSet(viewsets.ModelViewSet):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer

    def list(self, request, *args, **kwargs):
        self.pagination_class = None  # Disable pagination
        return super().list(request, *args, **kwargs)
