from db.db_manager import DBManager

class BluetoothDeviceDAO(DBManager):
    def __init__(self):
        super().__init__()

    def add_bluetooth_device(self, user_id, mac_address, device_name):
        sql = """
            INSERT INTO bluetooth_devices (user_id, mac_address, device_name)
            VALUES (%s, %s, %s)
        """
        params = (user_id, mac_address, device_name)
        return self.execute_bool(sql, params)

    def get_mac_by_user_id(self, user_id):
        sql = "SELECT mac_address FROM bluetooth_devices WHERE user_id = %s"
        params = (user_id,)
        return self.fetch_one(sql, params)

    def get_mac_addresses_by_user_ids(self, user_ids):
        if not user_ids:
            return {}
        placeholders = ','.join(['%s'] * len(user_ids))
        sql = f"SELECT user_id, mac_address FROM bluetooth_devices WHERE user_id IN ({placeholders})"
        params = tuple(user_ids)
        rows = self.fetch_all(sql, params)
        return {row['user_id']: row['mac_address'] for row in rows}

    def delete_bluetooth_device(self, user_id):
        sql = "DELETE FROM bluetooth_devices WHERE user_id = %s"
        params = (user_id,)
        return self.execute(sql, params)

