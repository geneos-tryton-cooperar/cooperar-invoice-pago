from trytond.model import Workflow, ModelView, ModelSQL
from trytond.pool import Pool
import datetime
from decimal import Decimal

__all__ = ['Invoice']

class Invoice(Workflow, ModelSQL, ModelView):
    'Invoice'
    __name__ = 'account.invoice'

    #Extiendo el metodo de pago de factura
    def pay_invoice(self, amount, journal, date, description,
            amount_second_currency=None, second_currency=None):

        linereturn = super(Invoice, self).pay_invoice(amount=amount,
            journal=journal, date=date, description=description,
            amount_second_currency=amount_second_currency, second_currency=second_currency)

        #Recorro lineas-> Productos
        for line in self.lines:
            #Suma Cuotas?
            if (line.product.suma_cuotas):
                #Veo la cantidad
                cantidad_cuotas = line.quantity
                #Creo Cuota/s
                Cuota = Pool().get('asociadas.cuota')
                cuota = Cuota()
                mes_anio_proxima_cuota = cuota.get_mes_anio_proxima_cuota(self.party)
                fecha_proxima_cuota = mes_anio_proxima_cuota.split('-')
                mes_proximo = int(fecha_proxima_cuota[0])
                anio_proximo = int(fecha_proxima_cuota[1])

                #import pudb;pu.db
                
                for i in range (1, int(cantidad_cuotas) + 1): 
                    cuotanueva = Cuota()
                    cuotanueva.mes = mes_proximo
                    cuotanueva.anio = anio_proximo
                    cuotanueva.monto = line.product.list_price
                    cuotanueva.fecha_pago = datetime.date.today()
                    cuotanueva.asociada = self.party
                    cuotanueva.pagada = True
                    cuotanueva.save()

                    if mes_proximo == 12:
                        mes_proximo = 1
                        anio_proximo += 1
                    else:
                        mes_proximo += 1

        return linereturn