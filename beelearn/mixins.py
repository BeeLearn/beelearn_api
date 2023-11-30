from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.exceptions import NotAcceptable
from rest_framework.mixins import ListModelMixin


class ContextMixin:
    @property
    def request(self) -> Request:
        return self.context.get("request")


class BulkDeleteMixin:
    @action(methods=["DELETE"], detail=False, url_path="bulk-delete")
    def bulk_delete(self, request: Request):
        ids = request.query_params.get("ids")

        if not ids:
            raise NotAcceptable({"ids": "ids is required in query params"})
        try:
            ids = list(map(int, ids.split(",")))
        except ValueError:
            raise NotAcceptable({"ids": "Invalid ids required a integer"})

        self.get_queryset().filter(pk__in=ids).delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


class BreadCrumbListModelMixin(ListModelMixin):
    filter_field: str

    def list(self, request):
        response = super().list(request)

        return Response(
            {
                "response": response.data,
                "breadcrumb": self.get_breadcrumb(),
            },
            status=status.HTTP_200_OK,
        )

    def get_breadcrumb(self):
        raise NotImplementedError(
            ".get_breadcrumb method from %s class is not overriden" % self.__class__
        )
