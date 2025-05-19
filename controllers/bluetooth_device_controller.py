from models import BluetoothDeviceDAO

class BluetoothDeviceController:
    def __init__(self):
        self.bluetooth_dao = BluetoothDeviceDAO()

    def register_enrollment(self, user_id, mac_addr, name):
        return bool(self.bluetooth_dao.add_bluetooth_device(user_id, mac_addr, name))
