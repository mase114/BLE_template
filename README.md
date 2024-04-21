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

### 例

16 進数とする。
“変更” → 0x〇〇 (○には、数字や記号)

## I/O ピン入出力設定

```python
"""
入出力設定
"""
```

### 解説

I/O(入出力)ピンは、マイコンチップ上の物理的な端子であり、外部のデバイスや回路との接点です。
これらのピンは、マイコンが外部と通信し、制御するための主要な手段です。
詳しくは MicroPython ライブラリ machine---ハードウェア関連の関数を参照
[クラス Pin -- I/O ピンの制御](https://micropython-docs-ja.readthedocs.io/ja/latest/library/machine.Pin.html)

### 例

出力設定 Pin(25,Pin.OUT)

入力設定 Pin(25,Pin.IN,Pin.PULL_DOWN)

*番号はピン番号
*プルアップの場合は PULL_UP に変更

## Usage

## Features

## Reference

## Author
