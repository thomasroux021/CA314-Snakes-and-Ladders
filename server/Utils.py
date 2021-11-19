class Utils:
    @staticmethod
    def all(event, data = None, type = 'FOR_ALL'):
        if data is None:
            return {'event': event, 'type': type}
        else:
            return {'event': event, 'data': data, 'type': type}

    @staticmethod
    def text_objects(text, font , clr , *kward):
        if len(kward)>0:
            textSurface = font.render(text, True, clr ,kward[0])
        else:
            textSurface = font.render(text, True, clr )
        return textSurface, textSurface.get_rect()
