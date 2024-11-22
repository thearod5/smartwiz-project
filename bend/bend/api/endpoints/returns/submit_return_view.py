import datetime

import requests
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from api.endpoints.returns.submit_return_serializer import SubmitReturnSerializer
from api.models import Return


class SubmitReturnView(APIView):
    def post(self, request):
        serializer = SubmitReturnSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return_id = serializer.validated_data['return_id']
        tax_return = get_object_or_404(Return, id=return_id)

        annual_income = tax_return.annual_income
        attended_school = tax_return.attended_school
        owned_home = tax_return.owned_home

        if annual_income < 0:
            raise Exception("Income should be greater than zero.")
        if attended_school is None:
            raise Exception("Attended school has not been filled out.")
        if owned_home is None:
            raise Exception("Owned home has not been filled out.")

        # Calculate deductions
        deductions: float = 18000 if owned_home else 14600
        taxable_income = max(0, annual_income - deductions)

        taxes_owed = calculate_taxes_owed(taxable_income)

        # Calculate refund
        credits = 1000 if attended_school else 0
        taxes_refunded = credits - taxes_owed

        # Prepare webhook payload
        webhook_url = "https://hooks.zapier.com/hooks/catch/9512086/2r5k356/"
        payload = {
            "annual_income": annual_income,
            "attended_school": attended_school,
            "owned_home": owned_home,
            "taxable_income": taxable_income,
            "taxes_owed": taxes_owed,
            "taxes_refunded": taxes_refunded,
            "timestamp": datetime.datetime.now().isoformat()
        }

        # Send data to the webhook
        try:
            response = requests.post(webhook_url, json=payload)
            response.raise_for_status()
            return Response(response.json(), status=status.HTTP_200_OK)
        except requests.RequestException as e:
            return Response({"error": "Failed to submit return", "details": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Calculate taxes owed using progressive tax brackets
def calculate_taxes_owed(income):
    brackets = [
        (11000, 0.10),
        (44725 - 11000, 0.12),
        (95375 - 44725, 0.22),
        (182100 - 95375, 0.24),
        (231250 - 182100, 0.32),
        (578125 - 231250, 0.35),
        (float('inf'), 0.37),
    ]
    taxes = 0
    for limit, rate in brackets:
        if income <= limit:
            taxes += income * rate
            break
        taxes += limit * rate
        income -= limit
    return taxes
