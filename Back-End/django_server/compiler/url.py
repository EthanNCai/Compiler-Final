from . import views
from django.urls import path

urlpatterns = [
    path('get_analysis_table',views.get_analysis_table, name="get_analysis_table")
]