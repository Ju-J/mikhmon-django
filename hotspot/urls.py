from django.urls import path
from .views import (
    RouterCreateView,
    RouterListView,
    HotspotUserCreateView,
    HotspotUserListView,
    VoucherCreateView,
    api_active_sessions,
    api_router_list,
    api_user_list,
    api_voucher_list,
    dashboard,
    toggle_user_status,
)

urlpatterns = [
    path("", dashboard, name="dashboard"),
    path("routers/", RouterListView.as_view(), name="router-list"),
    path("routers/new/", RouterCreateView.as_view(), name="router-new"),
    path("users/", HotspotUserListView.as_view(), name="user-list"),
    path("users/new/", HotspotUserCreateView.as_view(), name="user-new"),
    path("users/<int:pk>/toggle/", toggle_user_status, name="user-toggle"),
    path("voucher/", VoucherCreateView.as_view(), name="voucher-form"),
    path("api/routers/", api_router_list, name="api-router-list"),
    path("api/users/", api_user_list, name="api-user-list"),
    path("api/vouchers/", api_voucher_list, name="api-voucher-list"),
    path("api/sessions/", api_active_sessions, name="api-active-sessions"),
]
