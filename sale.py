# This file is part of sale_salesman module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.

from trytond.model import fields
from trytond.pool import PoolMeta
from trytond.transaction import Transaction
from trytond.pyson import Eval


__all__ = [
    'Sale',
]
__metaclass__ = PoolMeta


class Sale():
    __name__ = 'sale.sale'

    salesman = fields.Many2One('res.user', 'Salesman',
        states={
            'readonly': Eval('state') != 'draft',
            },
        depends=['state'])

    @staticmethod
    def default_salesman():
        return Transaction().user
