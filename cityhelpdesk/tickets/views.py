from rest_framework import serializers

from .models import Domicilio, Votante


# class DomicilioSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = Domicilio
#         fields = ('pk', 'calle', 'numero', 'colonia', 'ciudad', 'codigo_postal',
#                   'latitud', 'longitud', 'telefono', 'created', 'modified')
