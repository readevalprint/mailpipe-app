from django.conf.urls import include, url
from django.urls import path

from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache

from rest_framework.authtoken.views import obtain_auth_token
from mailpipe.views import EmailAccountViewSet, EmailViewSet
from rest_framework.urlpatterns import format_suffix_patterns

from rest_framework_extensions.routers import ExtendedSimpleRouter
router = ExtendedSimpleRouter()

router.register(r"emails", EmailAccountViewSet, base_name="email").register(
    r"msg",
    EmailViewSet,
    base_name="msg",
    parents_query_lookups=["account"],
)

urlpatterns = router.urls
