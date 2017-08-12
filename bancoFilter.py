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

class FilterExchangeCash(telegram.ext.BaseFilter):
    def filter(self, message):
        return message.text == 'Transferencias'

filter_exchange_cash = FilterExchangeCash()

class FilterNumberAccount(telegram.ext.BaseFilter):
    def filter(self, message):
        return message.text.isdigit()

filter_num_account = FilterNumberAccount()