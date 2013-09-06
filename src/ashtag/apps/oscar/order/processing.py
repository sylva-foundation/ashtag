from django.contrib import messages

from oscar.apps.order import processing
from oscar.apps.order.exceptions import InvalidOrderStatus, InvalidLineStatus

from ashtag.apps.core.models import EmailTemplate

class EventHandler(processing.EventHandler):

    def handle_shipping_event(self, order, event_type, lines, line_quantities, **kwargs):
        super(EventHandler, self).handle_shipping_event(order, event_type, lines, line_quantities, **kwargs)

        try:
            order.set_status(event_type.name)
            for line in lines:
                line.set_status(event_type.name)
        except (InvalidOrderStatus, InvalidLineStatus), e:
            messages.warning(str(e))

        if event_type.name == 'Shipped':
            EmailTemplate.send('order_shipped', [order.email], order=order, lines=lines)

