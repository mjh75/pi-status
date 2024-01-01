import time
import shutil
import psutil
from smbus import SMBus


class StatsDisplay:
    disks = []

    def __init__(self):
        pass

    def get_time(self):
        curdate = time.strftime("%A %B %d, %Y %H:%M:%S", time.localtime())
        return curdate

    def get_cpu(self):
        cpu = psutil.cpu_percent(interval=0.0, percpu=False)
        return cpu

    def get_temp(self):
        with open('/sys/class/thermal/thermal_zone0/temp') as temp:
            t = temp.read()
        temperature = int(t)/1000
        return temperature


    def get_battery(self):
        try:
            i2cbus = SMBus(1)
            i2caddress = 0x57
            battery = i2cbus.read_byte_data(i2caddress, 0x2a)
        except Exception as ex:
            battery = 0
        return battery


    def add_disk(self, path):
        self.disks.append(path)

    def get_disk(self):
        retval = []
        for disk in self.disks:
            _d = shutil.disk_usage(disk)
            _percent = round((_d.used / _d.total) * 100, 0)
            retval.append({'disk': disk, 'used': _percent})
        return retval


    def __init__(self):
        cpu = psutil.cpu_percent(interval=0.0, percpu=False)
