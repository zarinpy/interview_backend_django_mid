from rest_framework.response import Response
from rest_framework import generics

from interview.order.models import Order, OrderTag
from interview.order.serializers import OrderSerializer, OrderTagSerializer


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

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class OrderTagListCreateView(generics.ListCreateAPIView):
    queryset = OrderTag.objects.all()
    serializer_class = OrderTagSerializer
