class SerializerMixin:
    """
    Mixin pour la récupération de la classe de sérialiseur appropriée en fonction de l'action de vue.
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
        Retourne la classe de sérialiseur appropriée en fonction de l'action de vue.

        :return: Classe de sérialiseur.
        """
        return self.serializer_mapping.get(self.action, self.serializer_class)
