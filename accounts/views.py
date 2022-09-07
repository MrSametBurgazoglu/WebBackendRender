from django.shortcuts import get_object_or_404

from rest_framework import parsers, renderers
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.serializers import CustomerSerializer, AuthCustomTokenSerializer
from rest_framework.authtoken.models import Token
from accounts.models import Customer

class CustomerViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = CustomerSerializer
    queryset = Customer.objects.all()

    def get_permissions(self):
        if self.action in ["update", "partial_update", "destroy", "list", "retrieve"]:
            return (IsAuthenticated(),)
        else:
            return (AllowAny(),)

    @action(detail=True, methods=['post'])
    def change_state(self, request, pk=None):
        """
        change state of the user
        """
        customer = get_object_or_404(Customer, pk=pk)
        customer.active = not customer.active
        customer.save()
        return Response({"success": "True"})


class ObtainAuthToken(APIView):
    throttle_classes = ()
    permission_classes = ()
    parser_classes = (
        parsers.FormParser,
        parsers.MultiPartParser,
        parsers.JSONParser,
    )

    renderer_classes = (renderers.JSONRenderer,)

    def post(self, request):
        serializer = AuthCustomTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)

        return Response({'token': token.key})
