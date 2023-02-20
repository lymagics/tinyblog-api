from rest_framework import serializers

from ..models import User


class UserSerializer(serializers.ModelSerializer):
    """
    DRF serializer to represent User model.
    """

    class Meta:
        model = User
        read_only_fields = ('id', 'avatar_url', 'last_seen', 'first_seen',)
        fields = ('id', 'username', 'email', 'about_me',
                  'avatar_url', 'password', 'last_seen',
                  'first_seen',)
        extra_kwargs = {
            'password': {'write_only': True},
            'email': {'write_only': True},
        }

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class UpdateUserSerializer(UserSerializer):
    """
    DRF serializer to represent User model update schema.
    """
    old_password = serializers.CharField(max_length=50, required=False, write_only=True)

    class Meta(UserSerializer.Meta):
        fields = UserSerializer.Meta.fields + ('old_password',)

    def validate_old_password(self, value):
        if not self.instance.check_password(value):
            raise serializers.ValidationError('Invalid old password.')
        return value

    def validate(self, attrs):
        password = attrs.get('password', None)
        old_password = attrs.pop('old_password', None)
        if password is not None and (old_password is None):
            raise serializers.ValidationError({'old_password': 'Provide old password.'})
        return attrs

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)

        instance = super().update(instance, validated_data)

        if password is not None:
            instance.set_password(password)

        instance.save()
        return instance
