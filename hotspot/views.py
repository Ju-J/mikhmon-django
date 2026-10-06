from routeros_api import RouterOsApiPool
from routeros_api.exceptions import RouterOsApiError


class RouterOSClient:
    def __init__(self, router):
        self.router = router

    def connect(self):
        pool = RouterOsApiPool(
            username=self.router.username,
            password=self.router.password,
            host=self.router.host,
            port=self.router.port,
            use_ssl=self.router.use_ssl,
        )
        return pool.get_api()

    def test_connection(self):
        api = self.connect()
        try:
            api(cmd='/system/resource/print')
            return True
        except RouterOsApiError as exc:
            raise Exception(f'RouterOS connection failed: {exc}') from exc
        finally:
            api.close()

    def list_hotspot_users(self):
        api = self.connect()
        try:
            return api(cmd='/ip/hotspot/user/print')
        except RouterOsApiError as exc:
            raise Exception(f'RouterOS error: {exc}') from exc
        finally:
            api.close()

    def add_hotspot_user(self, username, password, profile='default', comment=''):
        api = self.connect()
        try:
            api(cmd='/ip/hotspot/user/add', name=username, password=password, profile=profile, comment=comment)
            return True
        except RouterOsApiError as exc:
            raise Exception(f'Failed to add user: {exc}') from exc
        finally:
            api.close()

    def disable_hotspot_user(self, username):
        api = self.connect()
        try:
            user = self._find_user_by_name(api, username)
            if user:
                api(cmd='/ip/hotspot/user/set', numbers=user['.id'], disabled='true')
            return True
        except RouterOsApiError as exc:
            raise Exception(f'Failed to disable user: {exc}') from exc
        finally:
            api.close()

    def enable_hotspot_user(self, username):
        api = self.connect()
        try:
            user = self._find_user_by_name(api, username)
            if user:
                api(cmd='/ip/hotspot/user/set', numbers=user['.id'], disabled='false')
            return True
        except RouterOsApiError as exc:
            raise Exception(f'Failed to enable user: {exc}') from exc
        finally:
            api.close()

    def remove_hotspot_user(self, username):
        api = self.connect()
        try:
            user = self._find_user_by_name(api, username)
            if user:
                api(cmd='/ip/hotspot/user/remove', numbers=user['.id'])
            return True
        except RouterOsApiError as exc:
            raise Exception(f'Failed to remove user: {exc}') from exc
        finally:
            api.close()

    def _find_user_by_name(self, api, username):
        users = api(cmd='/ip/hotspot/user/print', where=f'name={username}')
        if users:
            return users[0]
        return None

    def get_active_sessions(self):
        api = self.connect()
        try:
            return api(cmd='/ip/hotspot/active/print')
        except RouterOsApiError as exc:
            raise Exception(f'Failed to fetch active sessions: {exc}') from exc
        finally:
            api.close()

    def get_hotspot_profiles(self):
        api = self.connect()
        try:
            return api(cmd='/ip/hotspot/user/profile/print')
        except RouterOsApiError as exc:
            raise Exception(f'Failed to fetch hotspot profiles: {exc}') from exc
        finally:
            api.close()
