from .models import Sale

class PaymentService:

    def __init__(self, sale: Sale):
        self.sale = sale

    def process_payment(self):
        self.sale.payment_method