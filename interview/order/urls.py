
from django.urls import path
from rest_framework.routers import SimpleRouter
from interview.order.views import OrderListCreateView, OrderTagListCreateView, OrdersByTagView

router = SimpleRouter()
router.register('', OrderListCreateView, basename='order')

urlpatterns = [
    path('tags/', OrderTagListCreateView.as_view(), name='order-detail'),
    path('orders-by-tag/<int:tag_id>/', OrdersByTagView.as_view(), name='orders-by-tag'),
]
urlpatterns += router.urls
