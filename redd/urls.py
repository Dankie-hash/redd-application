from django.urls import path, include
from django.contrib import admin
from app.views import signup, login, logout


urlpatterns = [
            path('login/', login, name='login'),
            path('logout/', logout, name='logout'),
            path('signup/', signup, name='signup'),
            path('admin/', admin.site.urls),
            path('', include('app.urls')),

]
