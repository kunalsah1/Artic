from tkinter.font import names

from django.urls import path
from .views import (register_user, login_user, asset_handler, asset_group_handler, ticket_handler, building_handler,
                    floor_handler, unit_handler, category_handler, subcategory_handler, Users_handler,
                    ticket_status_handler, event_handler)


urlpatterns = [
    path('register/', register_user, name='register_user'),
    path('login/', login_user, name='login_user'),
    path('assets/', asset_handler, name='list_assets'),
    path('assets/<int:pk>', asset_handler, name='list_assets'),
    path('asset_groups/', asset_group_handler, name='asset_group_handler'),
    path('asset_groups/<int:pk>/', asset_group_handler, name='asset_group_detail'),
    path('tickets/', ticket_handler, name='tickets'),
    path('tickets/<int:pk>/', ticket_handler, name='tickets'),
    path('buildings/', building_handler, name='buildings'),
    path('buildings/<int:pk>/', building_handler, name='update_building'),
    path('floors/', floor_handler, name='floor_handler'),
    path('floors/<int:pk>/', floor_handler, name='floor_handler'),
    path('units/', unit_handler, name='get_units' ),
    path('units/<int:pk>', unit_handler, name='get_by_id'),
    path('category/', category_handler, name='create_category'),
    path('category/<int:pk>', category_handler, name='create_category'),
    path('sub_category/', subcategory_handler, name='create_subcategory'),
    path('sub_category/<int:pk>', subcategory_handler, name='subcategory_by_id'),
    path('user/', Users_handler, name='get_all_users'),
    path('ticket_status/', ticket_status_handler, name='ticket_statuses'),
    path('ticket_status/<int:pk>', ticket_status_handler, name='status_by_id'),
    path('event/', event_handler, name='events')
]
