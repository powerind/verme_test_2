class SimpleMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
