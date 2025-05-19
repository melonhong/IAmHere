from models import BluetoothDeviceDAO, LectureDAO

class BluetoothDeviceController:
    def __init__(self):
        self.bluetooth_dao = BluetoothDeviceDAO()
        self.lecture_dao = LectureDAO()

    def register_enrollment(self, user_id, mac_addr, name):
        return bool(self.bluetooth_dao.add_bluetooth_device(user_id, mac_addr, name))
    
    def get_mac_addr(self, lecture_id):
        professor_id = self.lecture_dao.get_professor_by_id(lecture_id)
        return self.bluetooth_dao.get_mac_by_user_id(professor_id)
