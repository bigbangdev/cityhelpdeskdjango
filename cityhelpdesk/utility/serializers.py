# coding=utf-8
"""
Utility Serializers
"""

from rest_framework.serializers import HyperlinkedModelSerializer


class HybridModelSerializer(HyperlinkedModelSerializer):
    """
    ModelSerializer which provides both a `url` and `id` field
    """

    def get_pk_field(self, model_field):
        return self.get_field(model_field)
