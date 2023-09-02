from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import generics
from rest_framework.views import APIView

from interview.order.models import Order, OrderTag
from interview.order.serializers import OrderSerializer, OrderTagSerializer, DeactivateOrderSerializer


# Create your views here.
class OrderListCreateView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def list(self, request, *args, **kwargs):
        start_embargo_date = kwargs.get("start_embargo_date", None)
        end_embargo_date = kwargs.get("end_embargo_date", None)
        queryset = self.get_queryset()
        if start_embargo_date:
            queryset = queryset.filter(embargo_date__gte=start_embargo_date)

        if end_embargo_date:
            queryset = queryset.filter(embargo_date__lte=start_embargo_date)

        serializer = self.serializer_class(queryset, many=True)

        return Response(serializer.data, 200)


class OrderTagListCreateView(generics.ListCreateAPIView):
    queryset = OrderTag.objects.all()
    serializer_class = OrderTagSerializer
