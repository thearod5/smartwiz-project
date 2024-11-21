import datetime

import requests
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from api.endpoints.returns.submit_return_serializer import SubmitReturnSerializer
from api.models import Return


class SubmitReturnView(APIView):
    def post(self, request):
        serializer = SubmitReturnSerializer(data=request.data)
        if serializer.is_valid():
            return_id = serializer.validated_data['return_id']
            try:
                tax_return = Return.objects.get(id=return_id)
            except Return.DoesNotExist:
                return Response({"error": "Return not found"}, status=status.HTTP_404_NOT_FOUND)

            # Simulate tax calculation
            tax_return.taxable_income = tax_return.annual_income - (18000 if tax_return.owned_home else 14600)
            tax_return.taxes_owed = max(0, tax_return.taxable_income * 0.22)  # Example tax rate
            tax_return.taxes_refunded = 1000 if tax_return.attended_school else 0
            tax_return.save()

            # Send data to the webhook
            webhook_url = "https://hooks.zapier.com/hooks/catch/9512086/2r5k356/"
            payload = {
                "name": f"{tax_return.user.first_name} {tax_return.user.last_name}",
                "address": tax_return.user.primary_address.display if tax_return.user.primary_address else "N/A",
                "email": tax_return.user.email,
                "annual_income": tax_return.annual_income,
                "attended_school": tax_return.attended_school,
                "owned_home": tax_return.owned_home,
                "taxable_income": tax_return.taxable_income,
                "taxes_owed": tax_return.taxes_owed,
                "taxes_refunded": tax_return.taxes_refunded,
                "timestamp": datetime.datetime.now().isoformat()
            }
            try:
                response = requests.post(webhook_url, json=payload)
                response.raise_for_status()
                return Response({"message": "Return submitted successfully"}, status=status.HTTP_200_OK)
            except requests.RequestException as e:
                return Response({"error": "Failed to submit return", "details": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
