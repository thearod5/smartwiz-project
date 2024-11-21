from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from app.endpoints.returns.return_serializer import ReturnSerializer
from app.models import Return


class ReturnView(APIView):
    def post(self, request):
        serializer = ReturnSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, return_id):
        try:
            tax_return = Return.objects.get(id=return_id)
        except Return.DoesNotExist:
            return Response({"error": "Return not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = ReturnSerializer(tax_return, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
