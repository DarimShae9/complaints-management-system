from .models import Order, Message
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


def historic_entry(order_id, user, message):
    """
    We add an entry to the history of changes to the order
    """
    Message.objects.create(
        user=user,
        order=Order.objects.get(pk=order_id),
        text=message,
        creation_date=datetime.now()
    )
    return True
