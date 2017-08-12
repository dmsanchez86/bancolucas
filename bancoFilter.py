import telegram.ext

class FilterServices(telegram.ext.BaseFilter):
    def filter(self, message):
        return message.text == 'Ver nuestros servicios'

filter_service = FilterServices()

class FilterNewAccount(telegram.ext.BaseFilter):
    def filter(self, message):
        return message.text == 'Crear cuenta'

filter_new_account = FilterServices()