################################################################################
# 製作日 2023.12.29
# BLE相互通信Central側プログラム Rev.1.0.3
# 注意項目
# マイコンに書き込む場合、"template.py" → "main.py"に変更。
# ble_advertising.pyを同じディレクトリ内に保存。
# Switch Service UUID and Switch Characteristic UUIDの値を変更。(他機体と同値禁止)
# Switch Service UUID and Switch Characteristic UUIDの値をPeripheral側と同値
# 動作させる場合、スイッチ入力確認をコメントにしておく
################################################################################

import ubluetooth
import struct
import utime
import math
from micropython import const
from machine import Pin, I2C ,time_pulse_us,PWM
from ble_advertising import decode_services, decode_name

_IRQ_CENTRAL_CONNECT = const(1)
_IRQ_CENTRAL_DISCONNECT = const(2)
_IRQ_GATTS_WRITE = const(3)
_IRQ_GATTS_READ_REQUEST = const(4)
_IRQ_SCAN_RESULT = const(5)
_IRQ_SCAN_DONE = const(6)
_IRQ_PERIPHERAL_CONNECT = const(7)
_IRQ_PERIPHERAL_DISCONNECT = const(8)
_IRQ_GATTC_SERVICE_RESULT = const(9)
_IRQ_GATTC_SERVICE_DONE = const(10)
_IRQ_GATTC_CHARACTERISTIC_RESULT = const(11)
_IRQ_GATTC_CHARACTERISTIC_DONE = const(12)
_IRQ_GATTC_DESCRIPTOR_RESULT = const(13)
_IRQ_GATTC_DESCRIPTOR_DONE = const(14)
_IRQ_GATTC_READ_RESULT = const(15)
_IRQ_GATTC_READ_DONE = const(16)
_IRQ_GATTC_WRITE_DONE = const(17)
_IRQ_GATTC_NOTIFY = const(18)
_IRQ_GATTC_INDICATE = const(19)

_ADV_IND = const(0x00)
_ADV_DIRECT_IND = const(0x01)
_ADV_SCAN_IND = const(0x02)
_ADV_NONCONN_IND = const(0x03)

# Switch Service UUID
_SWITCH_SERVICE_UUID = ubluetooth.UUID("変更")

# Switch Characteristic UUID
_SWITCH_CHAR = (
    ubluetooth.UUID("変更"),
    ubluetooth.FLAG_READ | ubluetooth.FLAG_NOTIFY,
)

_SWITCH_SERVICE = (
    _SWITCH_SERVICE_UUID,
    (_SWITCH_CHAR),
)

#I/Oピン入出力設定
"""
  入出力設定
"""


class BLESwitchCentral:
    def __init__(self, ble):
        self._ble = ble
        self._ble.active(True)
        self._ble.irq(self._irq)
        self._reset()
        self._led = Pin('LED', Pin.OUT)

    def _reset(self):
        self._name = None
        self._addr_type = None
        self._addr = None
        self._value1 = None
        self._scan_callback = None
        self._conn_callback = None
        self._read_callback = None
        self._notify_callback = None
        self._conn_handle = None
        self._start_handle = None
        self._end_handle = None
        self._value_handle = None

    def _irq(self, event, data):
        if event == _IRQ_SCAN_RESULT:
            addr_type, addr, adv_type, rssi, adv_data = data
            if adv_type in (_ADV_IND, _ADV_DIRECT_IND):
                type_list = decode_services(adv_data)
                if _SWITCH_SERVICE_UUID in type_list:
                    self._addr_type = addr_type
                    self._addr = bytes(addr)
                    self._name = decode_name(adv_data) or "?"
                    self._ble.gap_scan(None)
        elif event == _IRQ_SCAN_DONE:
            if self._scan_callback:
                if self._addr:
                    self._scan_callback(self._addr_type, self._addr, self._name)
                    self._scan_callback = None
                else:
                    self._scan_callback(None, None, None)
        elif event == _IRQ_PERIPHERAL_CONNECT:
            conn_handle, addr_type, addr = data
            if addr_type == self._addr_type and addr == self._addr:
                self._conn_handle = conn_handle
                self._ble.gattc_discover_services(self._conn_handle)
        elif event == _IRQ_PERIPHERAL_DISCONNECT:
            conn_handle, _, _ = data
            if conn_handle == self._conn_handle:
                self._reset()
        elif event == _IRQ_GATTC_SERVICE_RESULT:
            conn_handle, start_handle, end_handle, uuid = data
            if conn_handle == self._conn_handle and (
                uuid == _SWITCH_SERVICE_UUID
            ):
                self._start_handle, self._end_handle = start_handle, end_handle
        elif event == _IRQ_GATTC_SERVICE_DONE:
            if self._start_handle and self._end_handle:
                self._ble.gattc_discover_characteristics(
                    self._conn_handle, self._start_handle, self._end_handle
                )
            else:
                print(" スイッチサービスが見つかりませんでした。")
        elif event == _IRQ_GATTC_CHARACTERISTIC_RESULT:
            conn_handle, def_handle, value_handle, properties, uuid = data
            if conn_handle == self._conn_handle and (
                uuid == _SWITCH_CHAR[0]
            ):
                self._value_handle = value_handle
            
        elif event == _IRQ_GATTC_CHARACTERISTIC_DONE:
            if self._value_handle:
                if self._conn_callback:
                    self._conn_callback()
            else:
                print("スイッチ特性の検索に失敗しました。")
        elif event == _IRQ_GATTC_READ_RESULT:
            conn_handle, value_handle, c_data = data
            if conn_handle == self._conn_handle:
                
                if value_handle == self._value_handle:
                    self._update_value1(c_data)
                    if self._read_callback:
                        self._read_callback(self._value1)
                        
        elif event == _IRQ_GATTC_READ_DONE:
            conn_handle, value_handle, status = data
        elif event == _IRQ_GATTC_NOTIFY:
            conn_handle, value_handle, notify_data = data
            if conn_handle == self._conn_handle:
                if value_handle == self._value_handle:
                    self._update_value1(notify_data)
                    if self._notify_callback:
                        self._notify_callback(self._value1)

    def is_connected(self):
        return self._conn_handle is not None and self._value_handle is not None
    
    def scan(self, callback=None):
        self._addr_type = None
        self._addr = None
        self._scan_callback = callback
        self._ble.gap_scan(2000, 10000, 30000)

    def connect(self, addr_type=None, addr=None, callback=None):
        self._addr_type = addr_type or self._addr_type
        self._addr = addr or self._addr
        self._conn_callback = callback
        if self._addr_type is None or self._addr is None:
            return False
        self._ble.gap_connect(self._addr_type, self._addr)
        return True

    def disconnect(self):
        if not self._conn_handle:
            return
        self._ble.gap_disconnect(self._conn_handle)
        self._reset()

    def read1(self, callback):
        if not self.is_connected():
            return
        self._read_callback = callback
        try:
            self._ble.gattc_read(self._conn_handle, self._value_handle)
        except OSError as error:
            pass
        except TypeError as error:
            pass

    def on_notify(self, callback):
        self._notify_callback = callback

    def _update_value1(self, data):
        try:
            self._value1 = struct.unpack("変更", data)   #少数の場合はfを使用
        except OSError as error:
            print(error)

    def value1(self):
        return self._value1

# スイッチ動作処理
def switch_value(sw):  
    print("read switch" ,sw)    #スイッチ入力確認
    """
    スイッチ動作処理
    """
def demo(ble, central):
    not_found = False

    def on_scan(addr_type, addr, name):
        if addr_type is not None:
            print("Found switch: %s" % name)
            central.connect()
        else:
            nonlocal not_found
            not_found = True
            print("No switch found.")

    central.scan(callback=on_scan)

    while not central.is_connected():
        if not_found:
            return

    print("Connected")

    while central.is_connected():
        central.read1(callback=switch_value)
    
    print("Disconnected")


if __name__ == "__main__":
    ble = ubluetooth.BLE()
    central = BLESwitchCentral(ble)
    while True:
        demo(ble, central)
        utime.sleep_us(3)
