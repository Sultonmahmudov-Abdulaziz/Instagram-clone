from django.urls import path
from .views import SingUpApiView


urlpatterns = [
    path('sing-up/', SingUpApiView.as_view, name="singup")
]