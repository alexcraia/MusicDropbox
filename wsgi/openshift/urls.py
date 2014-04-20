from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^$', 'openshift.views.home', name='home'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'login/', 'dropboxConnect.views.login'),
    url(r'register/', 'dropboxConnect.views.register_user'),
)
