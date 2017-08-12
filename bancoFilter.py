import telegram.ext


class FilterSi(telegram.ext.BaseFilter):

    def filter(self, message):
        return message.text ==  'Si'



filter_si = FilterSi()


class FilterServices(telegram.ext.BaseFilter):
    def filter(self, message):
        return message.text == 'Ver nuestros servicios'

filter_service = FilterServices()