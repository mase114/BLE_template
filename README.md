# BLE_template

## BLEとはなに？

BLEはBluetooth Low Energyの略で、低消費電力の無線通信技術です。Bluetoothの一種で、主に小型のデバイスやセンサーなどで利用されています。

[BLEについて](https://www.musen-connect.co.jp/blog/course/trial-production/ble-beginner-1/)

# Peripheral側BLEプログラムコード基本的使い方

## UUIDの設定方法

```python
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
```

## Requirement

## Usage

## Features

## Reference

## Author
