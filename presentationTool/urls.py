"""presentationTool URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin

from impressGenerator.views import index, add_page, remove_page, edit_page, download, new_presentation

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^add-page/', add_page, name='add-page'),
    url(r'^edit-page/', edit_page, name='edit-page'),
    url(r'^remove-page/', remove_page, name='remove-page'),
    url(r'^new-presentation/', new_presentation, name='new-presentation'),
    url(r'^download-(\d+)/', download, name='download'),
    url(r'^$', index, name='index')
]
