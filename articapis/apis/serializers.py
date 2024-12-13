from django.contrib.auth.models import User
from django.core.mail import send_mail
from rest_framework import serializers
from .models import Asset, AssetGroup, Building, Floor, Units, Categories, SubCategory, TicketStatus, Event


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    date_joined = serializers.DateTimeField(read_only=True)
    user_type = serializers.ChoiceField(choices=[('admin', 'Admin'), ('employee', 'Employee')], default='employee')

    class Meta:
        model = User
        fields = ['email', 'password','is_active', 'date_joined', 'user_type']

    def create(self, validated_data):

        is_active = validated_data.pop('is_active', True)

        email = validated_data['email']
        password = validated_data['password']
        username = email.split('@')[0]
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )
        user.is_active = is_active

        user.save()
        self.send_welcome_email(user.email, password)

        return user

    def send_welcome_email(self, email, password):
        subject = "Welcome to artic"
        message = f"Hello,\n\nThank you for registering. Here are your login credentials:\nEmail: {email}\nPassword: {password}\n\nBest regards,\nThe Team"
        send_mail(
            subject,
            message,
            'sahkunal94@gmail.com',
            [email],
            fail_silently=False
        )

class AssetSerializer(serializers.ModelSerializer):

    class Meta:
        model = Asset
        fields = '__all__'


# class AssetSerializer(serializers.ModelSerializer):
#     username = serializers.CharField(source='user.username', read_only=True)  # Add the username field for GET requests
#
#     class Meta:
#         model = Asset
#         fields = '__all__'  # Include all fields in the model
#
#     def to_representation(self, instance):
#         """
#         Customizing the GET representation to show the username instead of the user ID.
#         """
#         representation = super().to_representation(instance)
#         if self.context['request'].method == 'GET':
#             representation.pop('user')  # Remove the user field in GET responses
#         return representation

class AssetGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssetGroup
        fields = '__all__'

class BuildingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Building
        fields = '__all__'

class FloorSerializer(serializers.ModelSerializer):
    building_name = serializers.CharField(source='building_id.name', read_only=True)


    class Meta:
        model = Floor
        fields = '__all__'




class UnitSerializer(serializers.ModelSerializer):
    # floor_name = serializers.SerializerMethodField()
    floor_name = serializers.CharField(source='floor_id.name', read_only=True)
    building_name = serializers.CharField(source='building_id.name', read_only=True)
    class Meta:
        model = Units
        fields = '__all__'

    # def get_floor_name(self, obj):
    #     return obj.floor_id.name if obj.floor_id else None


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Categories
        fields = '__all__'

class SubCategorySerializer(serializers.ModelSerializer):
    category = serializers.CharField(source='category_id.name', read_only=True)
    class Meta:
        model = SubCategory
        fields = '__all__'


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"

class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketStatus
        fields = "__all__"


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields ="__all__"