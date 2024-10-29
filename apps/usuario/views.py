from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from apps.authentication.jwt_authentication import CustomJWTAuthentication
from .models import Permiso
from .serializers import PermisoSerializer


class ListPermiso(APIView):
    authentication_classes = [CustomJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            permisos = Permiso.objects.all()
            serializer = PermisoSerializer(permisos, many=True)

            return Response(
                {"payload": serializer.data, "detail": "OK", "api_status": True},
                status=status.HTTP_200_OK,
            )

        except Exception as error:
            return Response(
                {"payload": [], "detail": str(error), "api_status": False},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
