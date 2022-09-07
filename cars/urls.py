from django.urls import include, path

from rest_framework import routers

from cars import views

app_name = 'cars'

router = routers.DefaultRouter()
router.register(r'cars', views.CarsViewSet, basename="cars")

urlpatterns = [
    path('', include(router.urls)),
]