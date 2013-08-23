from django.utils.translation import ugettext_lazy as _
from django.http import HttpResponse
from django.utils.datastructures import SortedDict
from django.template.defaultfilters import date as format_date

from oscar.apps.dashboard.orders import views
from oscar.apps.dashboard.reports.csv_utils import CsvUnicodeWriter

class OrderListView(views.OrderListView):

    def download_selected_orders(self, request, orders):
        response = HttpResponse(mimetype='text/csv')
        response['Content-Disposition'] = 'attachment; filename=%s' % self.get_download_filename(request)
        writer = CsvUnicodeWriter(response, delimiter=',')

        meta_data = (('number', _('Order number')),
                     ('value', _('Order value')),
                     ('date', _('Date of purchase')),
                     ('num_items', _('Number of items')),
                     ('status', _('Order status')),
                     ('customer', _('Customer email address')),
                     ('shipping_address', _('Shipping address')),
                     ('billing_address', _('Billing address')),
                     )
        columns = SortedDict()
        for k, v in meta_data:
            columns[k] = v

        writer.writerow(columns.values())
        for order in orders:
            row = columns.copy()
            row['number'] = order.number
            row['value'] = order.total_incl_tax
            row['date'] = format_date(order.date_placed, 'DATETIME_FORMAT')
            row['num_items'] = order.num_items
            row['status'] = order.status
            row['customer'] = order.email

            if order.shipping_address:
                row['shipping_address'] = order.shipping_address
            else:
                row['shipping_address'] = ''
            if order.billing_address:
                row['billing_address'] = order.billing_address
            else:
                row['billing_address'] = ''

            encoded_values = [unicode(value).encode('utf8') for value in row.values()]
            writer.writerow(encoded_values)
        return response

# Called from the store.models
def setup_views():
    from oscar.apps.dashboard.orders import app
    app.application.order_list_view = OrderListView
