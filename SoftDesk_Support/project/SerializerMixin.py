class SerializerMixin:
    """
    Mixin for retrieving the appropriate serializer class
    according to the view action.
    """

    serializer_mapping = {
        "list": None,
        "retrieve": None,
        "create": None,
        "update": None,
        "partial_update": None,
    }

    def get_serializer_class(self):
        """
        Returns the appropriate serializer class according to the view action.

        :return: serializer class
        """
        return self.serializer_mapping.get(self.action, self.serializer_class)
