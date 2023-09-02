
from django.urls import path
from interview.order.views import OrderListCreateView, OrderTagListCreateView, DeactivateOrderView


urlpatterns = [
    path('deactivate/', DeactivateOrderView.as_view(), name='order-deactivate'),
    path('tags/', OrderTagListCreateView.as_view(), name='order-detail'),
    path('', OrderListCreateView.as_view(), name='order-list'),
]
