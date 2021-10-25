from django.shortcuts import render

from django.shortcuts import render
from rest_framework.views import APIView
from .models import WebsiteData
from .serializers import WebsiteSerializer
from rest_framework.response import Response

from bs4 import BeautifulSoup
import requests
from rest_framework import status
from bs4.element import Comment
from collections import Counter  

# Create your views here.




def tag_visible(element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True


def text_from_html(body):
    soup = BeautifulSoup(body, 'html.parser')
    texts = soup.findAll(text=True)
    visible_texts = filter(tag_visible, texts)  
    return u" ".join(t.strip() for t in visible_texts)
  




class WebsiteCreateList(APIView):
    """
    View for website create list api
    """
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
            context['data'] = []
            context['status'] = False
            status_code = status.HTTP_400_BAD_REQUEST
            context['message'] = str(e)
            return Response(context, status=status_code)
            
            
class WebsiteRetrive(APIView):
    """
    view for website retrive update and delete using website name.
    """
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
        else:
            context['data'] = []
            context['status'] = False
            status_code = status.HTTP_400_BAD_REQUEST
            context['message'] = "NO website found"
            return Response(context, status=status_code)
        
    def put(self, request,website_name):
        context = {}
        
        context['data'] = []
        context['status'] = True
        status_code =   501
        context['message'] = "Update Request"
        return Response(context, status=status_code)
              
        
    def delete(self, request, website_name):
        context = {}
        try:
            obj = self.get_object(website_name)
            if obj:
                obj.delete()
                context['data'] = []
                context['status'] = True
                status_code = 200
                context['message'] = "website data deleted"
                return Response(context, status=status_code)
                
            else:
                return Response({'mesg': "NO website found"},
                    status=404)
        except Exception as e:
            context['data'] = []
            context['status'] = False
            status_code = status.HTTP_400_BAD_REQUEST
            context['message'] = str(e)
            return Response(context, status=status_code)
 
            
class WebsiteWordRetrive(APIView):
    """
    View for get page most n th common word
    """
    def get_object(self, website_name):
        try:
            obj = WebsiteData.objects.get(website_name=website_name)
            return obj
        except Exception as e:
            return False
    
    def get(self, request,website_name, num):
        context = {}
        data = []
        obj = self.get_object(website_name)
        if obj:
            website_html = obj.website_html
            text = text_from_html(website_html)
            split_it = text.split()
            counter = Counter(split_it)
  
            most_occur = counter.most_common(int(num))
            result = dict(most_occur)
            data.append(result)
        
            context['data'] = data
            context['status'] = True
            status_code = status.HTTP_201_CREATED
            context['message'] = "Retrive WEbsite most common words"
            return Response(context, status=status_code)
        else:
            context['data'] = []
            context['status'] = False
            status_code = status.HTTP_400_BAD_REQUEST
            context['message'] = "NO website found"
            return Response(context, status=status_code)
        
        
class RetriveCommonWordView(APIView):
    """
    VIew for get most common word from all database website
    """
    def get(self, request, num):
        context = {}
        data = []
        texts = ""
        obj = WebsiteData.objects.all()
        if obj:
            for i in obj:
                website_html = i.website_html
                text = text_from_html(website_html)
                texts = texts + ' ' + text
                
            split_it = texts.split()
            counter = Counter(split_it)
            most_occur = counter.most_common(int(num))
            result = dict(most_occur)
            data.append(result)
        
            context['data'] = data
            context['status'] = True
            status_code = status.HTTP_201_CREATED
            context['message'] = "Retrive WEbsite most common words"
            return Response(context, status=status_code)