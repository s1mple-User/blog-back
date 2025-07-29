
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
from .views import CreateUser,MyTokenObtainPairView,BlogListAPIView,BlogsAPIView,BlogDetailAPIView,AuthorListAPIView,LogoutView,BlogsByAuthorAPIView,BlogAll

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/token', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh', TokenRefreshView.as_view(), name='token_refresh'), 

    path("api/auth/user",AuthorListAPIView.as_view()),
    path('api/auth/logout', LogoutView.as_view(), name='logout'),

    path("api/blog/get_all", BlogAll.as_view()),
    path("api/auth/author/<int:author_id>/",BlogsByAuthorAPIView.as_view()),

    path("api/auth/register",CreateUser.as_view(),name="register"),
    path("api/blog/create",BlogListAPIView.as_view()),
    path("api/blog/<slug:slug>",BlogDetailAPIView.as_view()),
    path("api/blog/search/",BlogsAPIView.as_view())
]