"""
URL configuration for proj project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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

import Stolari.views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

    path('admin/', admin.site.urls),
    path('', Stolari.views.login, name='login'),
    path('logout/', Stolari.views.logout_view, name='logout'),
    path('userProfile/', Stolari.views.user_profile_view, name='user_profile'),
    path('register.html', Stolari.views.register_render, name='register_render'),
    path('register/', Stolari.views.register, name='register'),
    path('explore.html', Stolari.views.explore_render, name='explore_render'),
    path('prikaziExplore/', Stolari.views.prikaziExplore, name='prikaziExplore'),
    path('prikaziExplore/prikaziStranicuObjekta/<int:idobj>/', Stolari.views.prikaziStranicuObjekta, name='prikaziStranicuObjekta'),
    path('prikaziExplore/prikaziStranicuObjekta/<int:idobj>/add_favorites/', Stolari.views.add_favorites, name='add_favorites'),
    path('prikaziExplore/prikaziStranicuObjekta/<int:idobj>/delete_favorites/', Stolari.views.delete_favorites, name='delete_favorites'),
    path('prikaziOmiljene/', Stolari.views.prikaziOmiljene, name='prikaziOmiljene'),
    path('prikaziExplore/prikaziStranicuObjekta/<int:idobj>/oceni_objekat/', Stolari.views.oceni_objekat, name='oceni_objekat'),
    path('prikaziExplore/prikaziStranicuObjekta/<int:idobj>/reservePlace/', Stolari.views.reservePlace,name='reservePlace')

]

