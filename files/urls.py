from django.urls import path
from .views import upload_file_view

app_name = "file"

urlpatterns = [
    # path('', upload_file_view, name = 'upload_view'),
    path('google', upload_file_view, name = 'upload'),

]