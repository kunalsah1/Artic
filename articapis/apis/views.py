from django.core.serializers import serialize
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from .serializers import RegisterSerializer, AssetSerializer, AssetGroupSerializer, BuildingSerializer, FloorSerializer, \
    UnitSerializer, CategorySerializer, SubCategorySerializer, UserListSerializer, StatusSerializer, EventSerializer
from .ticketSerializer import TicketSerializer
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from .models import Asset, AssetGroup, Ticket, Building, Floor, Units, Categories, SubCategory, TicketStatus
from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny
# Register user
@api_view(['POST'])
def register_user(request):
    if request.method == 'POST':
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            # Generate a token for the new user
            token, created = Token.objects.get_or_create(user=user)
            return Response({"message": "User created successfully", "token": token.key}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['POST'])
@permission_classes([AllowAny])
def login_user(request):
    email = request.data.get('email')
    password = request.data.get('password')

    if not email or not password:
        return Response({"error": "Email and password are required"})

    try:
        user = User.objects.get(email=email)

        if user.check_password(password):

            if user.is_active:

                token, created = Token.objects.get_or_create(user=user)
                return Response({
                    "message": "Login successfully",
                    "token": token.key,
                    "user_id": user.id,
                    "email": user.email,
                    "username": user.username
                }, status=status.HTTP_200_OK)
            else:
                return Response({"error": "User account is disabled"}, status=status.HTTP_403_FORBIDDEN)
        else:
            return Response({"error": "Invalid email or password"},status=status.HTTP_401_UNAUTHORIZED)
    except User.DoesNotExist:
        return Response({"error": "User with this email does not exist"}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def Users_handler(request):
    users = User.objects.all()
    serializer = UserListSerializer(users, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_asset(request):
    if request.method == 'POST':
        serializer = AssetSerializer(data=request.data)
        if serializer.is_valid():
            group_id = request.data.get('group')
            group = AssetGroup.objects.get(id=group_id)
            serializer.save(user=request.user,group=group)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def asset_handler(request, pk=None):
    if request.method == 'GET':
        group = request.query_params.get('group')  # Use 'group' for consistency
        if pk:
            try:
                assets = Asset.objects.get(pk=pk)
                serializer = AssetSerializer(assets)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Asset.DoesNotExist:
                return Response({"error": "Asset not found"}, status=status.HTTP_404_NOT_FOUND)

        # If 'group' is provided, filter assets by group
        if group:
            assets = Asset.objects.filter(group_id=group)
        else:
            assets = Asset.objects.all()

        serializer = AssetSerializer(assets, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)



    elif request.method == 'POST':
        serializer = AssetSerializer(data=request.data)
        if serializer.is_valid():
            group_id = request.data.get('group')
            if not group_id:
                return Response({"error": "Group ID is required"}, status=status.HTTP_400_BAD_REQUEST)

            try:
                group = AssetGroup.objects.get(id=group_id)
            except AssetGroup.DoesNotExist:

                return Response({"error": "Invalid Group ID: Group does not exist"}, status=status.HTTP_400_BAD_REQUEST)


            serializer.save(user=request.user, group=group)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'PUT':
        if pk is None:
            return Response({"error": "Asset id is required to update"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            asset = Asset.objects.get(pk=pk)
        except Asset.DoesNotExist:
            return Response({"error": "Asset not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = AssetSerializer(asset, request.data, partial=True)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        if pk is None:
            return Response({"error": "Asset id is required to delete"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            asset = Asset.objects.get(pk=pk)
            asset.delete()
            return Response({"message":"Asset deleted successfully"}, status=status.HTTP_205_RESET_CONTENT)
        except Asset.DoesNotExist:
            return Response({"error": "Asset not found"}, status=status.HTTP_404_NOT_FOUND)


# Asset group
@api_view(['GET', 'POST', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def asset_group_handler(request, pk=None):
    if request.method == 'GET':
        if pk:
            try:
                group = AssetGroup.objects.get(pk=pk)
                serializer = AssetGroupSerializer(group)
            except AssetGroup.DoesNotExist:
                return Response({"error": "Group not found"}, status=status.HTTP_404_NOT_FOUND)
        else:
            groups = AssetGroup.objects.all()
            serializer = AssetGroupSerializer(groups, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        serializer = AssetGroupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'PUT':
        if pk is None:
            return Response({"error": "Group id is required to update"}, status=status.HTTP_404_NOT_FOUND)
        try:
            group = AssetGroup.objects.get(pk=pk)
        except AssetGroup.DoesNotExist:
            return Response({"error": "Group not fount"}, status=status.HTTP_404_NOT_FOUND)

        serializer = AssetGroupSerializer(group, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        if pk is None:
            return Response({"error": "Group id is required to delete"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            group = AssetGroup.objects.get(pk=pk)
            group.delete()
            return Response({"message": "Group deleted successfully"}, status=status.HTTP_205_RESET_CONTENT)
        except AssetGroup.DoesNotExist:
            return Response({"error": "Group not found"}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET', 'POST', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def ticket_handler(request, pk=None):
    if request.method == 'GET':
        if pk:
            try:
                ticket = Ticket.objects.get(pk=pk)
                serializer = TicketSerializer(ticket)
            except Ticket.DoesNotExist:
                return Response({"error": "Ticket not found"}, status=status.HTTP_404_NOT_FOUND)
        else:
            tickets = Ticket.objects.all()
            serializer = TicketSerializer(tickets, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        serializer = TicketSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'PUT':
        if pk is None:
            return Response({"error": "Ticket id required to update"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            ticket = Ticket.objects.get(pk=pk)
        except Ticket.DoesNotExist:
            return Response({"error": "Ticket not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = TicketSerializer(ticket, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        if pk is None:
            return Response({"error": "Ticket id is required to delete"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            ticket = Ticket.objects.get(pk=pk)
            ticket.delete()
            return Response({"message": "Ticket deleted successfully"}, status=status.HTTP_205_RESET_CONTENT)
        except Ticket.DoesNotExist:
            return Response({"error": "Ticket not found"}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET', 'POST', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def building_handler(request, pk=None):
    if request.method == 'POST':
        serializer = BuildingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'GET':
        if pk:
            try:
                building = Building.objects.get(pk=pk)
                serializer = BuildingSerializer(building)
            except Building.DoesNotExist:
                return Response({"error": "Building not found"}, status=status.HTTP_404_NOT_FOUND)
        else:
            buildings = Building.objects.all()
            serializer = BuildingSerializer(buildings, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'PUT':
        if pk is None:
            return Response({"error": "Building id is required to update"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            building = Building.objects.get(pk=pk)
        except Building.DoesNotExist:
            return Response({"error": "building not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = BuildingSerializer(building, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'DELETE':
        if pk is None:
            return Response({"error": "Building id is required to delete"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            building = Building.objects.get(pk=pk)
            building.delete()
            return Response({"message": "Building deleted successfully"}, status=status.HTTP_205_RESET_CONTENT)
        except Building.DoesNotExist:
            return Response({"error": "Building not found"}, status=status.HTTP_404_NOT_FOUND)

# floor api
@api_view(['GET', 'POST', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def floor_handler(request, pk=None):
    if request.method == 'POST':
        serializer = FloorSerializer(data=request.data)
        if serializer.is_valid():
            building_id = request.data.get('building_id')
            if not building_id:
                return Response({"error":"Building id is required"}, status=status.HTTP_400_BAD_REQUEST)
            try:
                building = Building.objects.get(id=building_id)
            except Building.DoesNotExist:
                return Response({"error": "Invalid building id: building does not exist"}, status=status.HTTP_400_BAD_REQUEST)
            serializer.save(building_id=building)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'GET':
        if pk:
            try:
                floor = Floor.objects.get(pk=pk)
                serializer = FloorSerializer(floor)
            except Floor.DoesNotExist:
                return Response({'error': 'Floor not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            floors = Floor.objects.all()
            serializer = FloorSerializer(floors, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'PUT':
        if pk is None:
            return Response({"error": "Floor id is required"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            floor = Floor.objects.get(pk=pk)
        except Floor.DoesNotExist():
            return Response({"error": "Floor not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = FloorSerializer(floor, request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        if pk is None:
            return Response({"error": "Floor id is required to delete"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            floor = Floor.objects.get(pk=pk)
            floor.delete()
            return Response({"message": "Floor deleted successfully"}, status=status.HTTP_205_RESET_CONTENT)
        except Floor.DoesNotExist:
            return Response({'error': 'Floor not found'}, status=status.HTTP_205_RESET_CONTENT)


@api_view(['GET', 'POST', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def unit_handler(request, pk=None):
    if request.method == 'POST':
        serializer = UnitSerializer(data=request.data)
        if serializer.is_valid():
            floor_id = request.data.get('floor_id')
            building_id = request.data.get('building_id')
            if not floor_id:
                return Response({'error': 'floor id required'}, status=status.HTTP_400_BAD_REQUEST)
            try:
                floor = Floor.objects.get(id=floor_id)
            except Floor.DoesNotExist:
                return Response({'error': 'Invalid Floor id'}, status=status.HTTP_400_BAD_REQUEST)
            if not building_id:
                return Response({'error': 'building id is required'}, status=status.HTTP_400_BAD_REQUEST)
            try:
                building = Building.objects.get(id=building_id)
            except Building.DoesNotExist:
                return Response({'error': 'invalid building id'}, status=status.HTTP_400_BAD_REQUEST)
            serializer.save(floor_id=floor, building_id=building)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'GET':
        current_floor_id = request.query_params.get('current_floor_id')
        if pk:
            try:
                unit = Units.objects.get(pk=pk)
                serializer = UnitSerializer(unit)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Units.DoesNotExits:
                return Response({'error': 'unit not found'}, status=status.HTTP_404_NOT_FOUND)
        elif current_floor_id:
            units = Units.objects.filter(floor_id=current_floor_id)
            if units.exists():
                serializer = UnitSerializer(units, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'No units found for the specified floor ID'}, status=status.HTTP_404_NOT_FOUND)
        else:
            units = Units.objects.all()
            serializer = UnitSerializer(units, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'PUT':
        if pk is None:
            return Response({'error': 'Unit ID is required to update'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            unit = Units.objects.get(pk=pk)
        except Units.DoesNotExist:
            return Response({"error": "Unit not found"}, status=status.HTTP_404_NOT_FOUND)

        # Partial update with provided data
        serializer = UnitSerializer(unit, data=request.data, partial=True)
        if serializer.is_valid():
            # Handle optional floor_id update
            floor_id = request.data.get('floor_id')
            if floor_id:
                try:
                    floor = Floor.objects.get(id=floor_id)
                    unit.floor_id = floor
                except Floor.DoesNotExist:
                    return Response({'error': 'Floor not found'}, status=status.HTTP_404_NOT_FOUND)

            # Handle optional building_id update
            building_id = request.data.get('building_id')
            if building_id:
                try:
                    building = Building.objects.get(id=building_id)
                    unit.building_id = building
                except Building.DoesNotExist:
                    return Response({'error': 'Invalid Building ID'}, status=status.HTTP_400_BAD_REQUEST)

            # Save updated data
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        # Return validation errors
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST', 'GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def category_handler(request, pk=None):
    if request.method == 'POST':
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'GET':
        if pk:
            try:
                category = Categories.objects.get(pk=pk)
                serializer = CategorySerializer(category)
            except Categories.DoesNotExist:
                return Response({"error": 'Category not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            categories = Categories.objects.all()
            serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'PUT':
        if pk is None:
            return Response({"error": "Category id is required to edit category"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            category = Categories.objects.get(pk=pk)
        except Categories.DoesNotExist :
            return Response({"error":"Category not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = CategorySerializer(category, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'DELETE':
        if pk is None:
            return Response({'error':"id is required"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            category = Categories.objects.get(pk=pk)
            category.delete()
            return Response({"message": "Category deleted successfully"}, status=status.HTTP_205_RESET_CONTENT)
        except Categories.DoesNotExist:
            return Response({"error": "Category not found"}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET', 'POST', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def subcategory_handler(request, pk=None):
    if request.method == 'POST':
        serializer = SubCategorySerializer(data=request.data)
        if serializer.is_valid():
            category_id = request.data.get('category_id')
            if not category_id:
                return Response({"error": 'category_id is required'}, status=status.HTTP_400_BAD_REQUEST)
            try:
                category = Categories.objects.get(id=category_id)
            except Categories.DoesNotExist():
                return Response({"error": "Invalid category id: category does not exist"}, status=status.HTTP_400_BAD_REQUEST)
            serializer.save(category_id=category)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'GET':
        category_id = request.query_params.get('category_id')
        if pk:
            try:
                subcategory = SubCategory.objects.get(pk=pk)
                serializer = SubCategorySerializer(subcategory)
            except SubCategory.DoesNotExist:
                return Response({"error": "Sub category not found"}, status=status.HTTP_404_NOT_FOUND)
        else:
            subcategories = SubCategory.objects.all()
            if category_id is not None:
                subcategories = subcategories.filter(category_id=category_id)
            serializer = SubCategorySerializer(subcategories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'PUT':
        if pk is None:
            return Response({'error': 'sub category id is required'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            subcategory = SubCategory.objects.get(pk=pk)
        except SubCategory.DoesNotExist:
            return Response({"error": "sub category not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = SubCategorySerializer(subcategory, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        if pk is None:
            return Response({'error': 'id is required to delete'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            subcategory = SubCategory.objects.get(pk=pk)
            subcategory.delete()
            return Response({'message': "Subcategory deleted successfully"})
        except SubCategory.DoesNotExist:
            return Response({'error': "Sub category not found"}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET', 'POST', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def ticket_status_handler(request, pk=None):
    if request.method == 'POST':
        serializer = StatusSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'GET':
        if pk:
            try:
                ticket_status = TicketStatus.objects.get(pk=pk)
                serializer = StatusSerializer(ticket_status)
            except TicketStatus.DoesNotExist:
                return Response({"error": "Status not found"}, status=status.HTTP_404_NOT_FOUND)
        else:
            ticket_statuses = TicketStatus.objects.all()
            serializer = StatusSerializer(ticket_statuses, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'PUT':
        if pk is None:
            return Response({"error": "status id is required to update"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            ticket_status = TicketStatus.objects.get(pk=pk)
        except TicketStatus.DoesNotExist:
            return Response({"error":"status not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = StatusSerializer(ticket_status, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        if pk is None:
            return Response({'error': "status id is required to update"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            ticket_status = TicketStatus.objects.get(pk=pk)
            ticket_status.delete()
            return Response({"message": "Ticket deleted successfully"})
        except TicketStatus.DoesNotExist:
            return Response({"error": "status not found"}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET', 'POST', 'DELETE', 'PUT'])
@permission_classes([IsAuthenticated])
def event_handler(request, pk=None):
    if request.method == 'POST':
        serializer = EventSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#shift show user names in response



