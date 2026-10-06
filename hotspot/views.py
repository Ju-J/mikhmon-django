from django.contrib import messages
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .forms import HotspotUserForm, RouterForm, VoucherForm
from .models import HotspotUser, RouterDevice, Voucher
from .routeros import RouterOSClient
from .serializers import HotspotUserSerializer, RouterDeviceSerializer, VoucherSerializer


def dashboard(request):
    routers = RouterDevice.objects.count()
    users = HotspotUser.objects.count()
    vouchers = Voucher.objects.count()
    return render(request, "dashboard.html", {"routers": routers, "users": users, "vouchers": vouchers})


class RouterListView(ListView):
    model = RouterDevice
    template_name = "routers.html"
    context_object_name = "routers"


class RouterCreateView(CreateView):
    model = RouterDevice
    form_class = RouterForm
    template_name = "router_form.html"
    success_url = reverse_lazy("router-list")


class HotspotUserListView(ListView):
    model = HotspotUser
    template_name = "users.html"
    context_object_name = "users"


class HotspotUserCreateView(CreateView):
    model = HotspotUser
    form_class = HotspotUserForm
    template_name = "user_form.html"
    success_url = reverse_lazy("user-list")

    def form_valid(self, form):
        obj = form.save(commit=False)
        router = obj.router
        client = RouterOSClient(router)
        try:
            client.add_hotspot_user(obj.username, obj.password, profile=obj.profile, comment=obj.comment)
            messages.success(self.request, "Hotspot user created successfully.")
        except Exception as exc:
            messages.error(self.request, str(exc))
            return redirect("user-list")
        obj.save()
        return super().form_valid(form)


class VoucherCreateView(CreateView):
    model = Voucher
    form_class = VoucherForm
    template_name = "voucher_form.html"
    success_url = reverse_lazy("voucher-form")

    def form_valid(self, form):
        messages.success(self.request, f"Voucher {form.cleaned_data['code']} created successfully.")
        return super().form_valid(form)


def toggle_user_status(request, pk):
    user = HotspotUser.objects.get(pk=pk)
    client = RouterOSClient(user.router)
    if user.disabled:
        client.enable_hotspot_user(user.username)
        user.disabled = False
    else:
        client.disable_hotspot_user(user.username)
        user.disabled = True
    user.save()
    messages.success(request, "User status updated.")
    return redirect("user-list")


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def api_router_list(request):
    routers = RouterDevice.objects.all()
    serializer = RouterDeviceSerializer(routers, many=True)
    return Response(serializer.data)


@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def api_user_list(request):
    if request.method == "GET":
        users = HotspotUser.objects.all()
        serializer = HotspotUserSerializer(users, many=True)
        return Response(serializer.data)

    serializer = HotspotUserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def api_voucher_list(request):
    vouchers = Voucher.objects.all()
    serializer = VoucherSerializer(vouchers, many=True)
    return Response(serializer.data)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def api_active_sessions(request):
    routers = RouterDevice.objects.filter(is_active=True)
    active_sessions = []
    for router in routers:
        try:
            client = RouterOSClient(router)
            sessions = client.get_active_sessions()
            for item in sessions:
                active_sessions.append({"router": router.name, "session": item})
        except Exception:
            continue
    return Response(active_sessions)
