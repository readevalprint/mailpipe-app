from rest_framework import serializers
from .models import Email, EmailAccount

from django.urls import reverse


class EmailSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.SerializerMethodField()
    text = serializers.CharField()
    html = serializers.CharField()
    to = serializers.CharField()
    frm = serializers.CharField()
    subject = serializers.CharField()
    # date = serializers.DateTimeField()
    account_url = serializers.HyperlinkedRelatedField(
        source="account",
        lookup_field="address",
        lookup_url_kwarg='address',
        view_name="email-detail",
        read_only=True,
    )
    account = serializers.SlugRelatedField(read_only=True, slug_field="address")

    def get_url(self, obj):
        request = self.context.get("request")
        return request.build_absolute_uri(
            reverse(
                "msg-detail",
                kwargs={"parent_lookup_account": obj.account.address, "pk": obj.pk}
            )
        )

    def get_attachments(self, obj):
        request = self.context.get("request")
        attachments = obj.attachments()
        if request:
            for v in attachments:
                v["attachment_url"] = request.build_absolute_uri(v["attachment_url"])
        return attachments

    attachments = serializers.SerializerMethodField()

    class Meta:
        model = Email
        fields = (
            "url",
            "id",
            "frm",
            "to",
            "subject",
            "text",
            "html",
            "attachments",
            "account_url",
            "account",
            "created_at",
        )


class EmailAccountSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="email-detail", lookup_field='address', lookup_url_kwarg='address')
    messages = serializers.HyperlinkedIdentityField(
        view_name="msg-list",
        lookup_field="address",
        lookup_url_kwarg="parent_lookup_account",
    )

    class Meta:
        model = EmailAccount
        fields = ("url", "address", "callback_url", "messages")
