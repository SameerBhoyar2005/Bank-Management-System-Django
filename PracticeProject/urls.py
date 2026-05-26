
from django.urls import path, include

from PracticeProject.views import index,date
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('hello/',index),
    path('date/', date),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/v1/',include('api.urls')),
    ]
