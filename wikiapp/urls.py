from django.urls import path
from . import views

app_name = 'wikiapp'

urlpatterns = [
    path('', views.search, name='home'),
    path('autocomplete/', views.autocomplete, name='ajax'),
    path('pdf_download/', views.pdf_download, name='pdf_download'),
    
]