from django.conf.urls import patterns, include, url
from django.contrib.auth.views import logout

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'user_admin.views.register'),
    url(r'accounts/login/', 'user_admin.views.login'),
    url(r'accounts/logout/', logout),
    url(r'create/profile/', 'user_admin.views.create_profile'),
    url(r'accounts/profile/', 'user_admin.views.profile'),
    url(r'user/settings/', 'user_admin.views.settings')

    # url(r'^tangol/', include('tangol.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
