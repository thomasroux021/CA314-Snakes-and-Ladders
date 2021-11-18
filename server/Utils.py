class Utils:
    @staticmethod
    def all(event, data = None, type = 'FOR_ALL'):
        if data is None:
            return {'event': event, 'type': type}
        else:
            return {'event': event, 'data': data, 'type': type}

