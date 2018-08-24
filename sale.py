# This file is part of sale_salesman module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.

from trytond.model import fields
from trytond.pool import PoolMeta, Pool
from trytond.transaction import Transaction
from trytond.pyson import Eval
from trytond import backend

__all__ = ['Sale']


class Sale(metaclass=PoolMeta):
    __name__ = 'sale.sale'

    employee = fields.Many2One('company.employee', 'Salesman',
        domain=[
            ('company', '=', Eval('company', -1)),
            ],
        states={
            'readonly': Eval('state') != 'draft',
            },
        depends=['state', 'company'])

    @classmethod
    def __register__(cls, module_name):
        pool = Pool()
        User = pool.get('res.user')

        cursor = Transaction().connection.cursor()
        TableHandler = backend.get('TableHandler')
        table = TableHandler(cls, module_name)

        super(Sale, cls).__register__(module_name)

        # Migration from 2.8: Salesman from user to employee
        if table.column_exist('salesman'):
            cursor.execute('update "%s" set employee = "%s".employee from "%s"'
                ' where "%s".id = "%s".salesman' %
                (cls._table, User._table,
                    User._table, User._table, cls._table))
            table.column_rename('salesman', 'salesman_deprecated')

    @staticmethod
    def default_employee():
        User = Pool().get('res.user')

        if Transaction().context.get('employee'):
            return Transaction().context['employee']
        else:
            user = User(Transaction().user)
            if user.employee:
                return user.employee.id
