from .models import WebsiteData
from rest_framework import serializers

class WebsiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = WebsiteData
        fields = ['id', 'website_name', 'website_html']