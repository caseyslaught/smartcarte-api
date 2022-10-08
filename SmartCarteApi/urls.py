
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('account/', include('account.urls')),
    path('cybersyn/', admin.site.urls),
]
