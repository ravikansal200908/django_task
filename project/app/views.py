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



            
