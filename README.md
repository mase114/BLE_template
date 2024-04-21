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

### 解説

スイッチサービスの UUID(識別子)を定義しています。UUID は、BLE デバイス上のサービスや特性を一意に識別するための値です。この行では、ubluetooth.UUID() 関数を使用して UUID を生成して います。実際の UUID は `"変更"` の部分に置き換える必要があります。
スイッチ特性のUUIDとフラグを定義しています。ここでは、特性のUUIDとして ubluetooth.UUID() 関数を使用して UUID を生成し、特性のフラグとして ubluetooth.FLAG_READ | ubluetooth.FLAG_NOTIFY を指定しています。これは、特性が読み取り可能であり、通知をサポートし ていることを示しています。実際の UUID は `"変更"` の部分に置き換える必要があります。


## Requirement

## Usage

## Features

## Reference

## Author
