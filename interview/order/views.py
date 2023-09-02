from rest_framework.response import Response
from rest_framework import generics
from rest_framework.decorators import action
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin, CreateModelMixin
from rest_framework.views import APIView
from interview.order.models import Order, OrderTag
from interview.order.serializers import OrderSerializer, OrderTagSerializer


# Create your views here.
class OrderListCreateView(GenericViewSet, ListModelMixin, CreateModelMixin):
    queryset = Order.objects.all()
    serializer_classes = {
        "list": OrderSerializer,
        "create": OrderSerializer,
        "tags": OrderTagSerializer,
    }

    def get_serializer_class(self):
        return self.serializer_classes[self.action]

    def list(self, request, *args, **kwargs) -> Response:
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

    @action(detail=True, methods=["get"])
    def tags(self, request, pk=None) -> Response:
        try:
            order = self.get_queryset().get(pk=pk)
        except Order.DoesNotExist:
            return Response({"detail": "Order not found."}, status=404)

        serializer = self.get_serializer(order.tags.all(), many=True)
        return Response(serializer.data)


class OrderTagListCreateView(generics.ListCreateAPIView):
    queryset = OrderTag.objects.all()
    serializer_class = OrderTagSerializer


class OrdersByTagView(APIView):
    def get(self, request, tag_id):
        try:
            tag = OrderTag.objects.get(pk=tag_id)
        except OrderTag.DoesNotExist:
            return Response({"detail": "Tag not found."}, status=400)

        orders = tag.orders.all()
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data, status=200)
