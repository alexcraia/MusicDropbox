from django.conf.urls import patterns, include, url
from dropboxConnect import views
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', views.index),
    url(r'^dropbox/$', views.get_dropbox_auth_flow),
    url(r'^dropbox-auth-finish/$', views.dropbox_auth_finish),
    url(r'^dropbox-auth-start/$', views.dropbox_auth_start),
)
