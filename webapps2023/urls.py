from django.contrib import admin
from django.urls import path, include
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from register import views as register_views

urlpatterns = [
                  path('', register_views.redirect_to_webapps2023),
                  path('webapps2023/', include([
                      path('admin/', admin.site.urls),
                      path('', include("register.urls")),
                      path('payapp/', include("payapp.urls")),
                  ]))] + staticfiles_urlpatterns(prefix=settings.STATIC_URL)
