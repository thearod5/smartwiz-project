from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from api.endpoints.items.item_serializer import ItemSerializer
from api.models import Return
from api.models.item import Item


class ItemView(APIView):
    """
    View to handle create, update, and delete operations for itemizations.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """
        Create a new itemization for a specific return.
        """
        data = request.data

        if "return_record" not in data:
            return Response(
                {"error": "Request does not have a return_id id."},
                status=status.HTTP_404_NOT_FOUND
            )

        # Fetch the Return object from the database
        return_record = get_object_or_404(Return, id=data.get('return_record'))

        # Verify that the Return belongs to the authenticated user
        if return_record.user != request.user:
            return Response(
                {"error": "You are not authorized to add itemizations to this return."},
                status=status.HTTP_403_FORBIDDEN
            )
        serializer = ItemSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        """
        Edit an existing itemization.
        """
        itemization = get_object_or_404(Item, id=request.data['id'])
        serializer = ItemSerializer(itemization, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, item_id):
        """
        Delete an itemization.
        :param request: The request to delete item.
        :param item_id: The item id.
        :return:
        """
        itemization = get_object_or_404(Item, id=item_id)
        if itemization.return_record.user != request.user:
            return Response(
                {"error": "You are not authorized to delete item on this return."},
                status=status.HTTP_403_FORBIDDEN
            )
        itemization.delete()
        return Response({"message": "Itemization deleted successfully."}, status=status.HTTP_204_NO_CONTENT)

    def get(self, request, return_id):
        """
        Returns items in return id.
        :param request: HTTP request.
        :param return_id: ID of return whose items are retrieved.
        :return: List of items in return.
        """
        tax_return = get_object_or_404(Return, id=return_id)
        if tax_return.user != request.user:
            return Response({"error": "You are not authorized to view this return."},
                            status=status.HTTP_403_FORBIDDEN)

        items = Item.objects.filter(return_record=tax_return)
        serializer = ItemSerializer(items, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
