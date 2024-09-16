from rest_framework import status

from accounts.serialzers import AuthenticationRequestSerializer
from commons.mixins import FixStatusMixin
from commons.throttles import AuthenticationRateThrottle
from commons.viewsets import CreateModelViewSet


class AuthenticationViewSet(FixStatusMixin, CreateModelViewSet):
    fix_status = status.HTTP_200_OK
    authentication_classes = []
    permission_classes = []
    throttle_classes = [AuthenticationRateThrottle]
    serializer_class = AuthenticationRequestSerializer
