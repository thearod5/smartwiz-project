from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from api.endpoints.returns.return_serializer import ReturnSerializer
from api.models import Return


class ReturnView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """
        Creates a new Return associated with the authenticated user.
        """
        serializer = ReturnSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()  # The serializer will set the user field automatically
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        """
        Updates an existing Return. The ID of the Return should be provided in the payload.
        """
        return_id = request.data.get('id')  # Extract the ID from the payload
        if not return_id:
            return Response({"error": "ID is required to update a return."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            tax_return = Return.objects.get(id=return_id)

            # Ensure the return belongs to the authenticated user
            if tax_return.user != request.user:
                return Response({"error": "You are not authorized to edit this return."},
                                status=status.HTTP_403_FORBIDDEN)

        except Return.DoesNotExist:
            return Response({"error": "Return not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = ReturnSerializer(tax_return, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        """
        Returns a list of Returns for the currently authenticated user.
        :param request: The HTTP request.
        :return: List of returns for authenticated user.
        """
        returns = Return.objects.filter(user=request.user)  # Query for returns owned by the authenticated user
        serializer = ReturnSerializer(returns, many=True)  # Serialize the list of returns
        return Response(serializer.data, status=status.HTTP_200_OK)
