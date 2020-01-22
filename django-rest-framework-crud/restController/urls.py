from django.urls import include, path, re_path
from . import views


urlpatterns = [
    path('executeAction/', views.ExecuteAction.as_view(), name='Action')
]