from django.conf.urls import include, url
from django.urls import path

from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache

from rest_framework.authtoken.views import obtain_auth_token
from mailpipe.views import EmailDetail, EmailAccountDetail, EmailAccountList, EmailList, Attachment
from rest_framework.urlpatterns import format_suffix_patterns


urlpatterns = [
    #path(r'^admin/',eadmin.site.urls),
    path('emails/', EmailList.as_view(), name='email-list'),
    path('emails/<int:pk>/', EmailDetail.as_view(), name='email-detail'),
    path('emails/<int:email_pk>/attachments/<content_id>/<name>',
        never_cache(Attachment.as_view()), name='email-attachment'),
    path('accounts/', EmailAccountList.as_view(), name='email-account-list'),
    path('accounts/<address>/', EmailAccountDetail.as_view(), name='email-account-detail'),

    path('get_token/', obtain_auth_token, name='get_token'),
]


