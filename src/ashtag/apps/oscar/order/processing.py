from django.contrib import messages

from oscar.apps.order import processing
from oscar.apps.order.exceptions import InvalidOrderStatus, InvalidLineStatus, InvalidShippingEvent

from ashtag.apps.core.models import EmailTemplate

class EventHandler(processing.EventHandler):

    def handle_shipping_event(self, order, event_type, lines, line_quantities, **kwargs):
        changes = False
        new_status = event_type.name
        try:
            if order.status != new_status:
                changes = True
            order.set_status(new_status)
            for line in lines:
                if line.status != new_status:
                    changes = True
                line.set_status(new_status)
        except (InvalidOrderStatus, InvalidLineStatus), e:
            raise InvalidShippingEvent(str(e))

        if not changes:
            raise InvalidShippingEvent('The select order lines are already marked as %s' % new_status)

        super(EventHandler, self).handle_shipping_event(order, event_type, lines, line_quantities, **kwargs)

        if event_type.name == 'Shipped':
            EmailTemplate.send('order_shipped', [order.email], order=order, lines=lines)

