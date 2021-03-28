"""next_trident_website URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import path, include
from brand_hunt import views
'''from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView'''

# 実はページを表示するだけならこのように1行で書くことが出来ます。
#index_view = TemplateView.as_view(template_name="registration/index.html")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.IndexView.as_view()),
    path('csv/', views.CSVView.as_view()),
    path('pdf/', views.PDFView.as_view()),
    path('brand_hunt/user_research/', views.UserResearchView.as_view()),
    path('brand_hunt/item_research/', views.ItemResearchView.as_view()),
    #path("", login_required(index_view), name="index"),
    #path('', include("django.contrib.auth.urls")),
    #path('', include("brand_hunt.urls")),
]
