# -*- coding: utf-8 -*-
import telegram.ext

class FilterServices(telegram.ext.BaseFilter):
    def filter(self, message):
        return message.text == 'Ver nuestros servicios'

filter_service = FilterServices()

class FilterNewAccount(telegram.ext.BaseFilter):
    def filter(self, message):
        return message.text == 'Crear cuenta'

filter_new_account = FilterNewAccount()

class FilterDesactivateAccount(telegram.ext.BaseFilter):
    def filter(self, message):
        return message.text == 'Desactivar cuenta'

filter_desactivate_account = FilterDesactivateAccount()

class FilterActivateAccount(telegram.ext.BaseFilter):
    def filter(self, message):
        return message.text == 'Activar cuenta'

filter_activate_account = FilterActivateAccount()


class FilterTransfer(telegram.ext.BaseFilter):
    def filter(self, message):
        return message.text == 'Tansferencia'

filter_transfer = FilterTransfer()

class FilterNumber(telegram.ext.BaseFilter):
    def filter(self, message):
        return message.text.isdigit()

filter_number = FilterNumber()

class FilterAddBalance(telegram.ext.BaseFilter):
    def filter(self, message):
        return message.text == "Add fondos"


filter_add_balance = FilterAddBalance()

class FilterGetBalance(telegram.ext.BaseFilter):
    def filter(self, message):
        return message.text == "Ver Saldo"

filter_get_balance = FilterGetBalance()
