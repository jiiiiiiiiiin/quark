import serial


class ANO_DT:
    def __init__(self):
        self.MYHWADDR = 0x05
        self.SWJADDR = 0xAF

        self.BYTE1 = lambda x: (x >> 8) & 0xff
        self.BYTE2 = lambda x: (x >> 0) & 0xff

        self.ser = serial.Serial("/dev/ttyS0", 115200)

    def send_sensor(self, roll, pitch, yaw):
        data_to_send = []

        data_to_send.append(0xAA)
        data_to_send.append(self.MYHWADDR)
        data_to_send.append(self.SWJADDR)
        data_to_send.append(0x01)
        data_to_send.append(12)

        _temp = int(roll * 100)
        data_to_send.append(self.BYTE1(_temp))
        data_to_send.append(self.BYTE2(_temp))

        _temp = int(pitch * 100)
        data_to_send.append(self.BYTE1(_temp))
        data_to_send.append(self.BYTE2(_temp))

        _temp = int(yaw * 100)
        data_to_send.append(self.BYTE1(_temp))
        data_to_send.append(self.BYTE2(_temp))

        data_to_send.append(0)
        data_to_send.append(0)
        data_to_send.append(0)
        data_to_send.append(0)

        data_to_send.append(0)
        data_to_send.append(0)

        sum_data = 0
        for i in data_to_send:
            sum_data += i

        data_to_send.append(sum_data % 256)
        self.ser.write(bytes(data_to_send))


if __name__ == '__main__':
    ano = ANO_DT()
    ano.send_sensor(10, 10, 10)
