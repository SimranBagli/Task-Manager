from tasks.views import (
    RegisterView,
    TaskCreateView,
    TaskUpdateView,
    TaskDeleteView,
    TaskCompleteView,
    BlacklistRefreshView)
from django.urls import path
from rest_framework_simplejwt import views as jwt_views

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path(
        'token/',
        jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path(
        'token/refresh/',
        jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path(
        'token/logout/',
        BlacklistRefreshView.as_view(), name='token_refresh'),
    path('tasks/create/', TaskCreateView.as_view(), name='create_task'),
    path('<int:pk>/update', TaskUpdateView.as_view(), name='update_task'),
    path('<int:pk>/delete', TaskDeleteView.as_view(), name='delete_task'),
    path('<int:pk>/complete', TaskCompleteView.as_view(), name='complete_task')
]
