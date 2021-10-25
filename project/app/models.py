from django.db import models

# Create your models here.

# class WebsiteData(models.Model):
    
#     website_name = models.CharField(max_length=255, unique=True),
#     website_html = models.TextField()
    
#     def __str__(self) -> str:
#         return str(self.website_name)
    
    
class WebsiteData(models.Model):
    website_name = models.CharField(max_length=255, unique=True)
    website_url = models.CharField(max_length=255, null=True, blank=True)
    website_html = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.website_name