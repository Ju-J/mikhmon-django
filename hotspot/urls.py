from datetime import timedelta

from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import CreateView, ListView, UpdateView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .forms import HotspotProfileForm, HotspotUserForm, RouterForm, VoucherForm
from .models import ActiveSession, HotspotProfile, HotspotUser, RouterDevice, Voucher
from .routeros import RouterOSClient
from .serializers import ActiveSessionSerializer, HotspotProfileSerializer, HotspotUserSerializer, RouterDeviceSerializer, VoucherSerializer


def dashboard(request):
    routers = RouterDevice.objects.count()
    users = HotspotUser.objects.count()
    vouchers = Voucher.objects.count()
    active_sessions = ActiveSession.objects.count()
    recent_routers = RouterDevice.objects.order_by('-created_at')[:5]
    return render(request, 'dashboard.html', {
        'routers': routers,
        'users': users,
        'vouchers': vouchers,
        'active_sessions': active_sessions,
        'recent_routers': recent_routers,
    })


class RouterListView(ListView):
    model = RouterDevice
    template_name = 'routers.html'
    context_object_name = 'routers'


class RouterCreateView(CreateView):
    model = RouterDevice
    form_class = RouterForm
    template_name = 'router_form.html'
    success_url = reverse_lazy('router-list')

    def form_valid(self, form):
        router = form.save()
        client = RouterOSClient(router)
        try:
            client.test_connection()
            messages.success(self.request, f'Connected to {router.name} successfully.')
        except Exception as exc:
            messages.warning(self.request, f'Created router, but connection test failed: {exc}')
        return super().form_valid(form)


class HotspotProfileListView(ListView):
    model = HotspotProfile
    template_name = 'profiles.html'
    context_object_name = 'profiles'


class HotspotProfileCreateView(CreateView):
    model = HotspotProfile
    form_class = HotspotProfileForm
    template_name = 'profile_form.html'
    success_url = reverse_lazy('profile-list')


class HotspotUserListView(ListView):
    model = HotspotUser
    template_name = 'users.html'
    context_object_name = 'users'


class HotspotUserCreateView(CreateView):
    model = HotspotUser
    form_class = HotspotUserForm
    template_name = 'user_form.html'
    success_url = reverse_lazy('user-list')

    def form_valid(self, form):
        obj = form.save(commit=False)
        client = RouterOSClient(obj.router)
        try:
            client.add_hotspot_user(obj.username, obj.password, profile=obj.profile, comment=obj.comment)
            messages.success(self.request, 'Hotspot user created on MikroTik successfully.')
        except Exception as exc:
            messages.error(self.request, str(exc))
            return redirect('user-list')
        obj.save()
        return super().form_valid(form)


class VoucherCreateView(CreateView):
    model = Voucher
    form_class = VoucherForm
    template_name = 'voucher_form.html'
    success_url = reverse_lazy('voucher-form')

    def form_valid(self, form):
        code = form.cleaned_data['code']
        messages.success(self.request, f'Voucher {code} created successfully.')
        return super().form_valid(form)


class VoucherListView(ListView):
    model = Voucher
    template_name = 'vouchers.html'
    context_object_name = 'vouchers'


class ActiveSessionListView(ListView):
    model = ActiveSession
    template_name = 'sessions.html'
    context_object_name = 'sessions'


class RouterUpdateView(UpdateView):
    model = RouterDevice
    form_class = RouterForm
    template_name = 'router_form.html'
    success_url = reverse_lazy('router-list')


def toggle_user_status(request, pk):
    try:
        user = HotspotUser.objects.get(pk=pk)
    except ObjectDoesNotExist:
        messages.error(request, 'User not found.')
        return redirect('user-list')

    client = RouterOSClient(user.router)
    if user.disabled:
        client.enable_hotspot_user(user.username)
        user.disabled = False
    else:
        client.disable_hotspot_user(user.username)
        user.disabled = True
    user.save()
    messages.success(request, 'User status updated.')
    return redirect('user-list')


def sync_sessions_from_routers(request):
    routers = RouterDevice.objects.filter(is_active=True)
    for router in routers:
        client = RouterOSClient(router)
        try:
            rows = client.get_active_sessions()
            for item in rows:
                ActiveSession.objects.update_or_create(
                    router=router,
                    username=item.get('user', item.get('name', 'unknown')),
                    ip_address=item.get('ip-address', item.get('ip', '0.0.0.0')),
                    mac_address=item.get('mac-address', item.get('mac', '00:00:00:00:00:00')),
                    defaults={'started_at': timezone.now()},
                )
        except Exception as exc:
            messages.warning(request, f'Failed to sync router {router.name}: {exc}')
    messages.success(request, 'Active sessions synced.')
    return redirect('session-list')


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def api_router_list(request):
    routers = RouterDevice.objects.all()
    serializer = RouterDeviceSerializer(routers, many=True)
    return Response(serializer.data)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def api_user_list(request):
    if request.method == 'GET':
        users = HotspotUser.objects.all()
        serializer = HotspotUserSerializer(users, many=True)
        return Response(serializer.data)

    serializer = HotspotUserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def api_voucher_list(request):
    if request.method == 'GET':
        vouchers = Voucher.objects.all()
        serializer = VoucherSerializer(vouchers, many=True)
        return Response(serializer.data)

    serializer = VoucherSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def api_active_sessions(request):
    sessions = ActiveSession.objects.all()
    serializer = ActiveSessionSerializer(sessions, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def api_profiles(request):
    profiles = HotspotProfile.objects.all()
    serializer = HotspotProfileSerializer(profiles, many=True)
    return Response(serializer.data)
