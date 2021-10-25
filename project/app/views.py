from django.shortcuts import render

from django.shortcuts import render
from rest_framework.views import APIView
from .models import WebsiteData
from .serializers import WebsiteSerializer
from rest_framework.response import Response

from bs4 import BeautifulSoup
import requests
from rest_framework import status

# Create your views here.


class WebsiteCreateList(APIView):
    
    def get(self, request):
        website = WebsiteData.objects.all()
        serializer = WebsiteSerializer(website, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        context = {}
        website_url = request.data.get('website_url')
        r = requests.get(website_url)
        request.data.update({"website_html": r.text})
        try:
            serializer = WebsiteSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                context['data'] = serializer.data
                context['status'] = True
                status_code = status.HTTP_201_CREATED
                context['message'] = "Website HTml saved"
                return Response(context, status=status_code)
        except Exception as e:
            print(e,'===============')
            
            
class WebsiteRetrive(APIView):
    def get_object(self, website_name):
        try:
            obj = WebsiteData.objects.get(website_name=website_name)
            return obj
        except Exception as e:
            return False
    
    def get(self, request,website_name):
        context = {}
        obj = self.get_object(website_name)
        if obj:
            serializer = WebsiteSerializer(obj)
            context['data'] = serializer.data
            context['status'] = True
            status_code = status.HTTP_201_CREATED
            context['message'] = "Retrive WEbsite"
            return Response(context, status=status_code)
            