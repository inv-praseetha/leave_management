from app.views import CreatingUser,UserUPdateDetail,LoginAPIview
from rest_framework_simplejwt.views import TokenRefreshView
from django.contrib import admin
from django.urls import path


urlpatterns = [
    path('admin/', admin.site.urls),
    path('create/',CreatingUser.as_view()),
    path('create/<int:id>/',UserUPdateDetail.as_view()),
    path('login/',LoginAPIview.as_view()),
     path('/token/refresh/',TokenRefreshView.as_view(),name='token_refresh'),
    
]
