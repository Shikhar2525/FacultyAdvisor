from django.urls import path
from . import views

urlpatterns = [
    path('upload_sheet', views.upload_sheet, name="upload_sheet"),
    path('get_sheet', views.get_sheet, name="get_sheet"),
    path('create_pdf', views.create_pdf, name="create_pdf"),
]
