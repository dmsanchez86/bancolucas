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