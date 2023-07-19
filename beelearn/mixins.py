from rest_framework.request import Request 

class ContextMixin:
    @property
    def request(self) -> Request:
        return self.context.get("request")
