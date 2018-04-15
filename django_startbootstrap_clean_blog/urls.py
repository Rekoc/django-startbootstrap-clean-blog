"""django_startbootstrap_clean_blog URL Configuration

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
from django.conf.urls import url, include
from django.urls import path
from django.contrib import admin
from django_startbootstrap_clean_blog import views
from django.conf.urls.static import static
from django.conf import settings
from ckeditor_uploader import urls as ckeditor_urls
from distutils.version import StrictVersion
from django import get_version
# from django.conf.urls.i18n import i18n_patterns

if StrictVersion(get_version()) < StrictVersion('2.0'):
    urlpatterns = [
        url(r'^admin/', admin.site.urls),
        url(r'^ckeditor/', include(ckeditor_urls)),
        url(r'^$', views.Index.as_view(), name='Index'),
        url(r'^about', views.About, name='About'),
        url(r'^contact', views.Contact, name='Contact'),
        url(r'^portfolio/', views.Portfolio, name='Portfolio'),
        url(r'^(?P<category_slug>[\w-]+)/(?P<post_slug>[\w-]+)/', views.ViewPost, name='Post'),
        url(r'^(?P<category_slug>[\w-]+)/', views.ViewCategory, name='Category')
    ]
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
else:
    urlpatterns = [
        url(r'^admin/', admin.site.urls),
        path('ckeditor/', include(ckeditor_urls)),
        url(r'^$', views.Index.as_view(), name='Index'),
        url(r'^about', views.About, name='About'),
        url(r'^contact', views.Contact, name='Contact'),
        url(r'^portfolio/', views.Portfolio, name='Portfolio'),
        path('<slug:category_slug>/<slug:post_slug>/', views.ViewPost, name='Post'),
        path('<slug:category_slug>/', views.ViewCategory, name='Category'),
    ]
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

