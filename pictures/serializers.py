from rest_framework import serializers

from pictures.models import Picture


class PictureSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        picture = Picture(**validated_data)
        picture.user = self.context['request'].user
        picture.save()
        return picture

    class Meta:
        model = Picture
        fields = [
            'id',
            'title',
            'file',
        ]
