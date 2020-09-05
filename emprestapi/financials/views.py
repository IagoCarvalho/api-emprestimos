from rest_framework.views import APIView
from rest_framework.response import Response


class ListLoans(APIView):
    def get(self, request):
        content = {'message': 'Hello, World!'}
        return Response(content)


# class ListLoan(generics.ListAPIView):
#     """
#     Lista todos os paises usados no Portal
#     """
#     queryset = Pais.objects.all()
#     serializer_class = PaisSerializer
#     permission_classes = (permissions.AllowAny,)