from django.urls import path
from .views import WebsiteCreateList, WebsiteRetrive, WebsiteWordRetrive,  RetriveCommonWordView

urlpatterns = [
    path('website', WebsiteCreateList.as_view(), name="website"),
    path('website/<str:website_name>', WebsiteRetrive.as_view(), name="retrive_website"),
    path('website/<str:website_name>/<int:num>', WebsiteWordRetrive.as_view(), name="retrive_website_common_word"),
    path('retrive_common_word/<int:num>', RetriveCommonWordView.as_view()),
]
