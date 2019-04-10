from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404

from .models import Email, EmailAccount
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import renderers, viewsets
from rest_framework.decorators import action

from rest_framework import authentication
from rest_framework.mixins import DestroyModelMixin
from . import serializers


class EmailAccountViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.EmailAccountSerializer
    lookup_field = "address"

    lookup_value_regex = "[^/]+"
    queryset = EmailAccount.objects.all()


class EmailViewSet(viewsets.ReadOnlyModelViewSet, DestroyModelMixin):
    serializer_class = serializers.EmailSerializer
    queryset = Email.objects.all()

    @action(detail=True, url_path=r"attachments/(?P<content_id>[^/.]+)/(?P<name>.*)")
    def attachment(self, request):
        email_pk = self.kwargs["email_address"]
        content_id = self.kwargs["content_id"]
        name = self.kwargs.get("name", None)
        email = self.get_object()
        attachment = email.raw_attachments()[content_id]
        if not attachment.get("filename", None) == name:
            return redirect(
                "msg-attachment",
                email_pk=email_pk,
                content_id=content_id,
                name=attachment["filename"],
            )

        response = HttpResponse(attachment["payload"])
        response["Content-Type"] = attachment["content_type"]
        # response['Content-Disposition'] = 'attachment; filename=%s' % attachment['filename']
        return response
