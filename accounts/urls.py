from django.urls import include, path
from rest_framework import routers, authtoken
from rest_framework.authtoken import views as auth_views
from accounts import views

app_name = 'accounts'

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet, basename="users")
router.register(r'customers', views.CustomerViewSet, basename="customers")


# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    #path('register/', views.RegisterUserAPIView.as_view()),
    path('api-token-auth/', auth_views.obtain_auth_token),
    #path('cars/', views.CarViewSet)
]