"""
URL configuration for apps project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import path
import stability
import springUTS.views
import stability.views
import stability.views_module.process_components as components

urlpatterns = [
    path('admin/', admin.site.urls),
    path('stability/', stability.views.app2, name = 'stability'),
    path('process_components/', components.process_components, name = 'process_components'),
    path('components_frontend/', stability.views.components_frontend, name = 'components_frontend'),
    path('springUTS/', springUTS.views.app, name = 'springUTS')
]