from .models import Order
from datetime import datetime


def update_modification_time(order_id):
    """
    we update the modification time with every change in the order
    :param order_id:
    :return:
    """
    order = Order.objects.get(pk=order_id)
    order.modification_date = datetime.now()
    order.save()
    return True
