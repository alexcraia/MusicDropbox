from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^$', 'dropboxConnect.views.index', name='index'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'login/', 'dropboxConnect.views.login'),
    url(r'register/', 'dropboxConnect.views.register_user'),
    url(r'first_connect/', 'dropboxConnect.views.first_connect'),
    url(r'select_music/', 'dropboxConnect.views.select_music'),
)
