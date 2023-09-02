
from django.urls import path
from rest_framework.routers import SimpleRouter
from interview.order.views import OrderListCreateView, OrderTagListCreateView

router = SimpleRouter()
router.register('', OrderListCreateView, basename='order')

urlpatterns = [
    path('tags/', OrderTagListCreateView.as_view(), name='order-detail'),
]
urlpatterns += router.urls
