# BLE_template

## BLEとはなに？

BLEはBluetooth Low Energyの略で、低消費電力の無線通信技術です。Bluetoothの一種で、主に小型のデバイスやセンサーなどで利用されています。

[BLEについて](https://www.musen-connect.co.jp/blog/course/trial-production/ble-beginner-1/)

# Central側BLEプログラムコード基本的使い方

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

`番号はピン番号`
`プルアップの場合は PULL_UP に変更`

## データのフォーマット設定

### 解説

```python
def _update_value1(self, data):
  try:
    self._value1 = struct.unpack("変更", data) #少数の場合は f を使用
  except OSError as error:
    print(error)
def value1(self):
  return self._value1
```

### 解説

データを解釈して保持し、それを取得するための手段を提供するために使用されます。以下にそれぞれ
のメソッドの役割と機能を解説します。

`_update_value1(self, data)`

このメソッドは、data という引数を受け取ります。この引数はバイト列(bytes)で、ある種のデータを 含んでいます。
メソッド内で、struct.unpack() 関数が使われています。これは、バイト列を指定されたフォーマットに 従って解釈し、Python のデータ型に変換するための関数です。
struct.unpack()の第一引数は、データのフォーマットを示す文字列です。struct.unpack()内はバイト列 がどのように構成されているかを示しています。各文字は特定のデータ型を表し、8 ビット符号なし整数 (B)、および 2 つの 32 ビット浮動小数点数(F)を解釈することを意味します。

### 例

整数1つと浮動小数点数1つの場合
`“変更”`→`“<BF”`(Peripheral 側から受信するスイッチの数および種類によって変化)

`””は削除しない`

## スイッチの動作処理

```python
# スイッチ動作処理
def switch_value(sw):
  #print("read switch" ,sw) #スイッチ入力確認
"""
スイッチ動作処理
"""
```

### 解説

スイッチの動作処理を行う関数です。スイッチの入力を確認して特定の処理を行います。
スイッチ入力を監視したい場合は、#print("read switch" ,sw)の#を削除します。プログラム完成後は、必 ずコメントに戻すこと。`(動作が重くなる為)`
スイッチ値は sw[0]〜sw[n]まで変数の中に格納されます。例えば、3つのスイッチの場合は sw[0]〜 sw[2]までの変数です。

### 例

タクトスイッチが押されている間だけ内蔵 LED を点灯させる。

```python
if sw[0] == 1:
  led.on()
else:
  led.off()
```

## 注意事項

マイコンに書き込む場合、"template.py" → "main.py"に変更。

ble_advertising.py を同じディレクトリ内に保存。

Switch Service UUID and Switch Characteristic UUID の値を変更。`(他機体と同値禁止)`

Switch Service UUID and Switch Characteristic UUID の値をPeripheral側と同値 

動作させる場合、スイッチ入力確認をコメントにしておく

# Peripheral側BLEプログラムコード基本的使い方

## UUIDの設定方法

[Central側BLEプログラムコード基本的使い方参照](https://github.com/mase114/BLE_template/blob/main/README.md#uuid%E3%81%AE%E8%A8%AD%E5%AE%9A%E6%96%B9%E6%B3%95)

##I/O ピン入出力設定

[Central側BLEプログラムコード基本的使い方参照]()

`Central 側と通信に使用するスイッチは次のスイッチ入力設定で設定すること。`


