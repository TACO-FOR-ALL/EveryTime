from django.urls import path

from . import views

"""
    URL prefix: /medias/
"""
urlpatterns = [
    path("callback",
         views.medias_oss_callback.as_view(),
         name='medias.oss.callback'),
]