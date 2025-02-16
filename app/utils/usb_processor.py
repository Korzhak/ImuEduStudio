from typing import Optional

from pyqtier.plugins import UsbDataProcessor


class DataProcessor(UsbDataProcessor):
    def __init__(self):
        super().__init__()
        self._buffer = ""
        self.START_MARKER = "$IMU:"

    @staticmethod
    def calculate_crc(data: str) -> int:
        checksum = 0
        for char in data:
            checksum ^= ord(char)
        return checksum & 0xFF

    def parse(self, data: bytes) -> Optional[dict]:
        try:
            self._buffer += data.decode()
        except UnicodeDecodeError:
            return None

        while True:
            # Шукаємо початок пакета
            start_idx = self._buffer.find(self.START_MARKER)
            if start_idx == -1:
                break

            # Шукаємо кінець пакету
            end_idx = self._buffer.find('\n', start_idx)
            if end_idx == -1:
                break

            # Вирізаємо повний пакет
            packet = self._buffer[start_idx:end_idx]
            self._buffer = self._buffer[end_idx + 1:]

            try:
                # Розділяємо дані та CRC
                data_part, crc_hex = packet.rsplit('*', 1)

                # Перевіряємо CRC
                calculated_crc = self.calculate_crc(data_part)
                received_crc = int(crc_hex, 16)

                if calculated_crc != received_crc:
                    print(f"CRC mismatch: calculated {calculated_crc:02X}, received {received_crc:02X}")
                    continue

                # Парсимо дані
                data_str = data_part[len(self.START_MARKER):]
                gyro_str, accel_str = data_str.split(';')

                gx, gy, gz = map(float, gyro_str.split(','))
                ax, ay, az = map(float, accel_str.split(','))

                result = {
                    'gyro': {'x': gx, 'y': gy, 'z': gz},
                    'accel': {'x': ax, 'y': ay, 'z': az}
                }
                return result
            except Exception as e:
                print(f"Error parsing packet: {e}")
                continue
        return None
