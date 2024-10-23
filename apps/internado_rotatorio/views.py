from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
from apps.authentication.jwt_authentication import CustomJWTAuthentication

from .models import Area, Tema
from .serializers import AreaAndTemaSerializer


class ListCreateTemaView(APIView):
    authentication_classes = [CustomJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            temas = Tema.objects.filter(is_status=True)

            serializer = AreaAndTemaSerializer(temas, many=True)

            return Response(
                {"payload": serializer.data, "detail": "OK", "api_status": True},
                status=status.HTTP_200_OK,
            )

        except Exception as e:
            return Response(
                {
                    "payload": {},
                    "detail": str(e),
                    "api_status": False,
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def post(self, request):
        try:
            serializer = AreaAndTemaSerializer(data=request.data)

            if serializer.is_valid():
                serializer.save()
                return Response(
                        {
                    "payload": serializer.data,
                    "detail": "Registor creado",
                    "api_status": True,
                },
                status=status.HTTP_201_CREATED,
                )
            else:
                return Response(
                        {
                    "payload": {},
                    "detail": "Verificar los campos.",
                    "api_status": False,
                },
                status=status.HTTP_422_UNPROCESSABLE_ENTITY
                )
        except Exception as e:
            return Response(
                {
                    "payload": {},
                    "detail": str(e),
                    "api_status": False,
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class DetailTemaView(APIView):
    authentication_classes = [CustomJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, area, uuid):
        try:
            exists_tema = Tema.objects.filter(
                is_status=True, area__name=area, uuid=uuid
            ).exists()

            if not exists_tema:
                return Response(
                    {
                        "payload": {},
                        "detail": "El tema seleccionado no existe.",
                        "api_status": False,
                    },
                    status=status.HTTP_404_NOT_FOUND,
                )
            # obtendemos el tema directamente por uuid ya no es necesario hacer otras verificiones
            # porque ya se iso en el codio de arriba
            temas = Tema.objects.get(uuid=uuid)
            serializer = AreaAndTemaSerializer(temas)

            return Response(
                {"payload": serializer.data, "detail": "OK", "api_status": True},
                status=status.HTTP_200_OK,
            )

        except Exception as e:
            return Response(
                {
                    "payload": {},
                    "detail": str(e),
                    "api_status": False,
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
