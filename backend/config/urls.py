"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from accounts import urls as accounts_urls
from projects import urls as projects_urls
from datasets import urls as datasets_urls
from generator import urls as generator_urls
from uploads import urls as uploads_urls
urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include(accounts_urls)),
    path('projects/', include(projects_urls)),
    path('datasets/', include(datasets_urls)),
    path('generator/',include(generator_urls)),
    path('uploads/',include(uploads_urls)),

]

if settings.DEBUG: urlpatterns+= static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)