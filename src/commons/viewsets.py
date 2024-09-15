from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet


class CreateRetrieveUpdateListModelViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.ListModelMixin,
    GenericViewSet
):
    """
    A viewset that provides create, retrieve, update, and list actions.
    """

    pass


class CreateModelViewSet(mixins.CreateModelMixin, GenericViewSet):
    """
    A viewset that provides create action.
    """
    pass


class RetrieveUpdateModelViewSet(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, GenericViewSet):
    """
    A viewset that provides retrieve and update actions.
    """
    pass


class CreateListModelViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, GenericViewSet):
    """
    A viewset that provides create and list actions.
    """
    pass


class UpdateModelViewSet(mixins.UpdateModelMixin, GenericViewSet):
    """
    A viewset that provides update action.
    """
    pass


class ListModelViewSet(mixins.ListModelMixin, GenericViewSet):
    """
    A viewset that provides list action.
    """
    pass


class RetrieveListModelViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, GenericViewSet):
    """
    A viewset that provides retrieve and list actions.
    """
    pass


class RetrieveUpdateListModelViewSet(
    mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.ListModelMixin, GenericViewSet
):
    """
    A viewset that provides retrieve, update, and list actions.
    """
    pass


class FixStatusMixin:
    """
    A mixin that allows to fix the status code of the response.
    """
    fix_status = None

    def finalize_response(self, request, response, *args, **kwargs):
        if self.fix_status is not None:
            response.status_code = self.fix_status
        return super().finalize_response(request, response, *args, **kwargs)
