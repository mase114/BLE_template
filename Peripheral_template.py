################################################################################
# 製作日 2023.12.29
# BlE相互通信Peripheral側プログラム Rev.1.0.2
# 注意項目
# マイコンに書き込む場合、"template.py" → "main.py"に変更。
# ble_advertising.pyを同じディレクトリ内に保存。
# Switch Service UUID and Switch Characteristic UUIDの値を変更。(他機体と同値禁止)
# Switch Service UUID and Switch Characteristic UUIDの値をCentral側と同値
# 動作させる場合、スイッチ入力確認をコメントにしておく
################################################################################

import ubluetooth
import struct
import utime
import ubinascii
from micropython import const
from machine import Pin,ADC
from ble_advertising import advertising_payload

_IRQ_CENTRAL_CONNECT = const(1)
_IRQ_CENTRAL_DISCONNECT = const(2)
_IRQ_GATTS_INDICATE_DONE = const(20)
_IRQ_GATTS_WRITE = const(3)

_FLAG_READ = const(0x0002)
_FLAG_NOTIFY = const(0x0010)
_FLAG_INDICATE = const(0x0020)

# Switch Service UUID
_SWITCH_SERVICE_UUID = ubluetooth.UUID("変更")

# Switch Characteristic UUIDs
_SWITCH_CHAR = (
    ubluetooth.UUID("変更"),
    _FLAG_NOTIFY | _FLAG_READ | _FLAG_INDICATE,
)

_SWITCH_SERVICE = (
    _SWITCH_SERVICE_UUID,
    (_SWITCH_CHAR,),
)

#I/Oピン入出力設定
"""
  入出力設定
"""

class BLESwitch:
    def __init__(self, ble, name=""):
        self._ble = ble
        self._ble.active(True)
        self._ble.irq(self._irq)
        
        #スイッチ入力設定
        """
         スイッチ入力設定
        """
        # Switch Service
        ((self._handle_switch,),) = self._ble.gatts_register_services((_SWITCH_SERVICE,))
        self._connections = set()

        if len(name) == 0:
            name = 'Pico %s' % ubinascii.hexlify(self._ble.config('mac')[1], ':').decode().upper()
        print('Switch name %s' % name)

        self._payload = advertising_payload(
            name=name, services=[_SWITCH_SERVICE_UUID]
        )
        self._advertise()

    def _irq(self, event, data):
        if event == _IRQ_CENTRAL_CONNECT:
            conn_handle, _, _ = data
            self._connections.add(conn_handle)
        elif event == _IRQ_CENTRAL_DISCONNECT:
            conn_handle, _, _ = data
            self._connections.remove(conn_handle)
            self._advertise()

    def _advertise(self, interval_us=500000):
        self._ble.gap_advertise(interval_us, adv_data=self._payload)

    def update_switch_state(self, notify=False, indicate=False):
        #スイッチ入力変数
        """
        変数記入
        """
        #スイッチ入力確認
        #print("Switch states:", "スイッチの変数を全て記入")
        
        #少数の場合はfを使用
        self._ble.gatts_write(self._handle_switch, struct.pack("変更", "スイッチの変数を全て記入"))

        # Notify/Indicate to all connected centrals for the Switch Characteristics
        if notify or indicate:
            for conn_handle in self._connections:
                if notify:
                    self._ble.gatts_notify(conn_handle, self._handle_switch)
                if indicate:
                    self._ble.gatts_indicate(conn_handle, self._handle_switch)

def demo():
    ble = ubluetooth.BLE()
    switch = BLESwitch(ble)

    while True:
        switch.update_switch_state(notify=True, indicate=False)

if __name__ == "__main__":
    demo()

