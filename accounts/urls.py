from django.urls import include, path
from rest_framework import routers
from accounts import views

app_name = 'accounts'

router = routers.DefaultRouter()
router.register(r'customers', views.CustomerViewSet, basename="customers")

urlpatterns = [
    path('', include(router.urls)),
    path('api-token-auth/', views.ObtainAuthToken().as_view()),
]
