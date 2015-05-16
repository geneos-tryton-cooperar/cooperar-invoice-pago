from trytond.pool import Pool
from .invoice import Invoice

def register():
    Pool.register(
        Invoice,
        module='cooperar-invoice-pago', type_='model')