from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.auth.views import login, logout

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'myproject.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^login', login),
    url(r'^logout', 'cms_users_put.views.mylogout'),
    url(r'^accounts/profile/', 'cms_users_put.views.view_info'),
    url(r'^cms/$', 'cms_users_put.views.view_info'),
    url(r'^cms/(\d+)', 'cms_users_put.views.content'),
    url(r'^(.*)', 'cms_users_put.views.msg_error'),
)
