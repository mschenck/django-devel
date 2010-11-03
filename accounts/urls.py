from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
#from django.contrib import admin
#admin.autodiscover()

urlpatterns = patterns('accounts.views',
    # Example:
    (r'^$', 'index'),
    (r'^index.html', 'index'),
    (r'^exists.html', 'exists'),
    (r'^confirmation.html', 'confirmation'),
    (r'^confirmed.html', 'confirmed'),
    (r'^signup.html', 'signup'),
    (r'^login.html', 'login'),
    (r'^logout.html', 'logout'),
    (r'^confirm/(?P<hash>\w+)$', 'confirm'),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # (r'^admin/(.*)', admin.site.root),
)
