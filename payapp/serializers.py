from django.urls import reverse
from django.utils.html import format_html
# from rest_framework import serializers
from . import models as test_models
# from LabProj import constants as backend_constants


# class ResultSerializer(serializers.ModelSerializer):
#     action = serializers.SerializerMethodField()
#
#     def get_action(self, result):
#         return """
#         <a class='btn btn-sm text-primary' href='{update}'><i class='fa fa-pen'></i></a>
#
#         <button class='btn btn-sm text-danger delete-btn' href='{delete}' onclick='delete_func(this)'><i class='fa fa-trash'></i></button>
#
#         <button class='btn btn-sm text-warning email-btn'  href='{id}' onclick='send_mail_and_sms(this)'><i class='fa fa-paper-plane'></i></button>
#         """.format(
#             update=reverse("edit-result", kwargs={"guid": result.guid}),
#             delete=reverse("delete-result", kwargs={"guid": result.guid}),
#             id=reverse("resend-email", kwargs={"guid": result.guid})
#         )
#
#     class Meta:
#         model = result_models.Result
#         fields = result_constants.table_fields_constants
#


# def test_serialzier_v2():
# class TestSerializerV2(serializers.ModelSerializer):
#     actions = serializers.SerializerMethodField()
#     icd = serializers.SerializerMethodField()
#
#     def get_icd(self, result):
#         return f'({result.icd})'
#
#     def get_actions(self, result):
#         return format_html("""
#                 <a class='btn btn-sm text-primary' href='{update}'><i class='fa fa-pen'></i></a>
#                 <button class='btn btn-sm text-danger delete-btn' href='{delete}' onclick='delete_func(this)'><i class='fa fa-trash'></i></button>
#                 """.format(
#             update=reverse("edit-test", kwargs={"id": result.id}),
#             delete=reverse("delete-test", kwargs={"id": result.id}),
#         )
#         )
#
#     class Meta:
#         model = test_models.Test
#         fields = backend_constants.test_fields  # + ['actions', ]

    # return TestSerializerV2
