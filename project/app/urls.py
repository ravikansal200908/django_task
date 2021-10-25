from django.urls import path, include
from .views import WebsiteCreateList, WebsiteRetrive

urlpatterns = [
    path('website', WebsiteCreateList.as_view(), name="website"),
    path('website/<str:website_name>', WebsiteRetrive.as_view(), name="retrive_website")
]
