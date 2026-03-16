# コア構文・データ型 — Python3リファレンス

> Python 3 エンジニア認定基礎試験 満点レベル対応

---

## §1. 基本データ型

### 1.1 数値型

```python
# int — 任意精度整数（メモリが許す限り無制限）
x = 10 ** 100          # 巨大整数も扱える
0b1010                 # 2進数 → 10
0o17                   # 8進数 → 15
0xFF                   # 16進数 → 255

# float — IEEE 754 倍精度浮動小数点（約15-17桁の有効数字）
3.14
1.0e-3                 # 0.001
float('inf')           # 正の無限大
float('nan')           # 非数

# complex — 複素数
z = 3 + 4j
z.real                 # 3.0
z.imag                 # 4.0
abs(z)                 # 5.0（絶対値）

# bool — True/False（intのサブクラス）
isinstance(True, int)  # True
True + True            # 2
```

### 1.2 数値演算

```python
7 / 2      # 3.5   真の除算（常にfloat）
7 // 2     # 3     切り捨て除算（整数除算）
7 % 2      # 1     剰余
2 ** 10    # 1024  べき乗
-7 // 2    # -4    負数の切り捨て除算（-∞方向へ丸め）★試験頻出
-7 % 2     # 1     Python: 除数の符号に一致（C言語と異なる）
divmod(7, 2)  # (3, 1)  商と余りを同時取得
```

### 1.3 型変換

```python
int("42")       # 42
int("FF", 16)   # 255（基数指定）
int(3.9)        # 3（切り捨て、四捨五入ではない）★
float("3.14")   # 3.14
str(42)         # "42"
bool(0)         # False
bool([])        # False
bool("0")       # True ★（非空文字列はTrue）
```

### 1.4 真偽値判定（Falsy値）★試験頻出

以下はすべて `False` と評価される:
```python
None             # None型
False            # bool
0, 0.0, 0j       # ゼロ数値
"", b""          # 空文字列・空バイト列
[], (), {}       # 空リスト・空タプル・空辞書
set()            # 空集合
range(0)         # 空range
```

それ以外はすべて `True`。カスタムクラスは `__bool__()` または `__len__()` で制御。

### 1.5 実務活用

```python
# 浮動小数点の比較 — ==は避ける
import math
0.1 + 0.2 == 0.3          # False ★
math.isclose(0.1 + 0.2, 0.3)  # True

# 金額計算にはDecimalを使う
from decimal import Decimal
Decimal("0.1") + Decimal("0.2") == Decimal("0.3")  # True

# 型チェック
isinstance(x, (int, float))   # 複数型の判定
type(x) is int                # 厳密な型一致（サブクラス除外）
```

---

## §2. 文字列

### 2.1 文字列リテラル

```python
# 通常の文字列
s = "hello"
s = 'hello'

# f-string（Python 3.6+）★推奨
name = "World"
f"Hello, {name}!"         # "Hello, World!"
f"{3.14159:.2f}"           # "3.14"
f"{1000:,}"               # "1,000"
f"{'hello':>10}"           # "     hello"（右寄せ）
f"{'hello':^10}"           # "  hello   "（中央寄せ）
f"{value!r}"               # repr()を呼ぶ

# format()メソッド
"Hello, {}!".format(name)
"{0} and {1}".format("a", "b")
"{name}".format(name="World")

# %演算子（旧式、レガシーコード用）
"Hello, %s! %d items" % (name, 5)

# raw文字列（バックスラッシュをエスケープしない）
r"C:\Users\new"            # バックスラッシュがそのまま

# マルチライン文字列
"""
複数行の
文字列
"""
```

### 2.2 スライス ★試験頻出

```python
s = "Python"
s[0]       # 'P'
s[-1]      # 'n'
s[1:4]     # 'yth'    （start <= x < stop）
s[:3]      # 'Pyt'    （先頭から3文字）
s[3:]      # 'hon'    （3番目以降）
s[::2]     # 'Pto'    （1つ飛ばし）
s[::-1]    # 'nohtyP' （逆順）★
s[1:5:2]   # 'yh'     （1から5まで2つ飛ばし）

# スライスは範囲外でもエラーにならない
s[0:100]   # 'Python' （はみ出し分は無視）
s[100]     # IndexError ★（インデックスアクセスはエラー）
```

### 2.3 主要メソッド

```python
# 分割・結合
"a,b,c".split(",")           # ['a', 'b', 'c']
"a,b,c".split(",", 1)        # ['a', 'b,c']（最大分割数）
",".join(["a", "b", "c"])    # "a,b,c"
"hello world".split()        # ['hello', 'world']（空白で分割）

# 検索・置換
"hello".find("ll")           # 2（見つからない場合-1）
"hello".index("ll")          # 2（見つからない場合ValueError）★
"hello".replace("l", "L")    # "heLLo"
"hello".count("l")           # 2
"hello".startswith("he")     # True
"hello".endswith("lo")       # True
"hello" in "hello world"     # True（in演算子）

# 変換
"Hello".upper()              # "HELLO"
"Hello".lower()              # "hello"
"hello world".title()        # "Hello World"
"hello world".capitalize()   # "Hello world"
"Hello".swapcase()           # "hELLO"

# 削除・詰め
"  hello  ".strip()          # "hello"
"  hello  ".lstrip()         # "hello  "
"  hello  ".rstrip()         # "  hello"
"###hello###".strip("#")     # "hello"

# 判定
"123".isdigit()              # True
"abc".isalpha()              # True
"abc123".isalnum()           # True
"  ".isspace()               # True

# 整形
"hello".center(11, "-")      # "---hello---"
"hello".ljust(10, ".")       # "hello....."
"hello".rjust(10, ".")       # ".....hello"
"42".zfill(5)                # "00042"
```

### 2.4 エンコーディング

```python
# str → bytes
"こんにちは".encode("utf-8")      # b'\xe3\x81\x93...'
"hello".encode("ascii")            # b'hello'

# bytes → str
b'\xe3\x81\x93'.decode("utf-8")   # 'こ'

# bytesリテラル
b"hello"                           # ASCII のみ
```

### 2.5 正規表現（reモジュール）

```python
import re

# 基本操作
re.match(r"^\d+", "123abc")     # <Match> （先頭マッチ）
re.search(r"\d+", "abc123def")  # <Match> （最初のマッチ）
re.findall(r"\d+", "a1b2c3")   # ['1', '2', '3']
re.sub(r"\d", "X", "a1b2")     # "aXbX"

# グループ
m = re.search(r"(\d+)-(\d+)", "Tel:03-1234")
m.group(0)    # "03-1234"（全体）
m.group(1)    # "03"
m.group(2)    # "1234"
m.groups()    # ("03", "1234")

# コンパイル（繰り返し使用時に高速化）
pattern = re.compile(r"\d+")
pattern.findall("a1b2c3")   # ['1', '2', '3']

# 主要メタ文字
# .  任意1文字（改行除く）
# ^  行頭      $  行末
# *  0回以上   +  1回以上   ?  0回か1回
# \d 数字      \w 英数字_   \s 空白
# \D 非数字    \W 非英数字  \S 非空白
# []  文字クラス   [^]  否定文字クラス
# |   OR          ()   グループ
# {n} n回         {n,m} n〜m回
```

### 2.6 実務活用

```python
# ログ解析
import re
log = '2026-03-16 10:30:45 ERROR Connection timeout'
m = re.match(r'(\d{4}-\d{2}-\d{2}) (\d{2}:\d{2}:\d{2}) (\w+) (.+)', log)
date, time, level, msg = m.groups()

# データクレンジング
def normalize_phone(s):
    digits = re.sub(r"[^\d]", "", s)
    return f"{digits[:3]}-{digits[3:7]}-{digits[7:]}"
```

---

## §3. リスト

### 3.1 基本操作

```python
# リストはミュータブル（変更可能）
lst = [1, 2, 3, "mixed", [4, 5]]
lst[0]        # 1
lst[-1]       # [4, 5]
lst[1:3]      # [2, 3]
len(lst)      # 5

# 要素の変更
lst[0] = 10
lst[1:3] = [20, 30, 40]   # スライスへの代入（長さ変更可）
```

### 3.2 主要メソッド

```python
lst = [3, 1, 4, 1, 5]

# 追加
lst.append(9)           # [3,1,4,1,5,9]（末尾に1要素追加）
lst.extend([2, 6])      # [...,9,2,6]  （イテラブルを展開して追加）
lst.insert(0, 0)        # [0,3,1,...]  （指定位置に挿入）
lst += [7]              # extendと同等

# 削除
lst.remove(1)           # 最初に見つかった1を削除（なければValueError）★
lst.pop()               # 末尾要素を削除して返す
lst.pop(0)              # 先頭要素を削除して返す
del lst[0]              # インデックス指定で削除
lst.clear()             # 全要素削除

# 検索
lst = [3, 1, 4, 1, 5]
lst.index(4)            # 2（なければValueError）
lst.count(1)            # 2（出現回数）
4 in lst                # True

# ソート
lst.sort()              # 昇順ソート（破壊的）★
lst.sort(reverse=True)  # 降順ソート（破壊的）
lst.reverse()           # 逆順（破壊的）

# 非破壊的ソート
sorted(lst)             # 新しいリストを返す ★
sorted(lst, key=abs)    # キー関数指定
sorted(lst, key=lambda x: x[1])  # ラムダ式
list(reversed(lst))     # 非破壊的逆順
```

### 3.3 リスト内包表記 ★試験頻出

```python
# 基本形
[x ** 2 for x in range(10)]           # [0, 1, 4, 9, ..., 81]

# 条件付き
[x for x in range(20) if x % 3 == 0]  # [0, 3, 6, 9, 12, 15, 18]

# if-else付き（条件式はforの前）
["even" if x % 2 == 0 else "odd" for x in range(5)]

# ネスト
[(x, y) for x in range(3) for y in range(3) if x != y]
# → [(0,1),(0,2),(1,0),(1,2),(2,0),(2,1)]

# 行列の転置
matrix = [[1, 2, 3], [4, 5, 6]]
[[row[i] for row in matrix] for i in range(3)]
# → [[1, 4], [2, 5], [3, 6]]

# 集合内包表記
{x % 3 for x in range(10)}            # {0, 1, 2}

# 辞書内包表記
{x: x**2 for x in range(5)}           # {0:0, 1:1, 2:4, 3:9, 4:16}

# ジェネレータ式（括弧のみ、メモリ効率的）
sum(x**2 for x in range(1000000))      # リストを生成しない
```

### 3.4 コピー ★試験頻出

```python
import copy

a = [[1, 2], [3, 4]]

# 浅いコピー（内部オブジェクトは共有）
b = a.copy()          # または list(a) または a[:]
b[0][0] = 99
a[0][0]               # 99 ★内部リストは共有される

# 深いコピー（再帰的にすべてコピー）
c = copy.deepcopy(a)
c[0][0] = 0
a[0][0]               # 99（影響しない）
```

### 3.5 実務活用

```python
# データ変換パイプライン
raw = ["  Alice, 30 ", "Bob, 25  ", "  Charlie, 35"]
records = [
    {"name": parts[0], "age": int(parts[1])}
    for line in raw
    for parts in [line.strip().split(", ")]
]

# フラット化
nested = [[1, 2], [3, 4], [5]]
flat = [x for sub in nested for x in sub]  # [1, 2, 3, 4, 5]
```

---

## §4. タプル

### 4.1 基本

```python
# タプルはイミュータブル（変更不可）
t = (1, 2, 3)
t = 1, 2, 3           # 括弧なしでもOK
t = (1,)               # 要素1つ — カンマ必須 ★
t = ()                 # 空タプル
t[0]                   # 1
t[0] = 10              # TypeError ★変更不可
```

### 4.2 パッキング/アンパッキング ★試験頻出

```python
# パッキング
t = 1, 2, 3

# アンパッキング
a, b, c = t               # a=1, b=2, c=3
a, *rest = [1, 2, 3, 4]   # a=1, rest=[2, 3, 4] ★
first, *mid, last = [1, 2, 3, 4, 5]  # first=1, mid=[2,3,4], last=5

# スワップ
a, b = b, a                # Pythonic なスワップ

# 関数からの複数戻り値
def divmod_custom(a, b):
    return a // b, a % b
q, r = divmod_custom(7, 3)
```

### 4.3 名前付きタプル

```python
from collections import namedtuple
from typing import NamedTuple

# collections.namedtuple
Point = namedtuple("Point", ["x", "y"])
p = Point(3, 4)
p.x                    # 3
p[0]                   # 3（インデックスアクセスも可）
p._asdict()            # {'x': 3, 'y': 4}

# typing.NamedTuple（型ヒント付き、推奨）
class Point(NamedTuple):
    x: float
    y: float
    z: float = 0.0     # デフォルト値
```

### 4.4 タプルとリストの使い分け

| 特性 | タプル | リスト |
|------|--------|--------|
| ミュータブル | No | Yes |
| ハッシュ可能 | Yes（要素次第） | No |
| 辞書キー | 使える | 使えない |
| メモリ | 少ない | 多い |
| 用途 | 固定データ、戻り値 | 可変コレクション |

### 4.5 実務活用

```python
# 辞書のキーに使う
location_data = {
    (35.6762, 139.6503): "Tokyo",
    (34.6937, 135.5023): "Osaka",
}

# 関数の複数戻り値
def analyze(data):
    return min(data), max(data), sum(data) / len(data)
low, high, avg = analyze([1, 2, 3, 4, 5])

# 定数データ
HTTP_METHODS = ("GET", "POST", "PUT", "DELETE")
```

---

## §5. 辞書

### 5.1 基本操作

```python
# dict: ハッシュテーブル実装（Python 3.7+で挿入順保持）
d = {"name": "Alice", "age": 30}
d = dict(name="Alice", age=30)         # 同等
d = dict([("name", "Alice"), ("age", 30)])

d["name"]              # "Alice"
d["email"]             # KeyError ★
d.get("email")         # None（KeyErrorにならない）
d.get("email", "N/A")  # "N/A"（デフォルト値）

# キーはハッシュ可能オブジェクトのみ（str, int, tuple等）
# リスト・辞書・集合はキーにできない ★
```

### 5.2 主要メソッド

```python
d = {"a": 1, "b": 2, "c": 3}

# アクセス
d.keys()               # dict_keys(['a', 'b', 'c'])
d.values()             # dict_values([1, 2, 3])
d.items()              # dict_items([('a',1), ('b',2), ('c',3)])

# 追加・更新
d["d"] = 4             # キー追加
d.update({"e": 5, "f": 6})   # 一括更新
d |= {"g": 7}          # マージ更新（Python 3.9+）

# 削除
del d["a"]             # キー削除（なければKeyError）
d.pop("b")             # 削除して値を返す（なければKeyError）
d.pop("x", None)       # なければデフォルト値
d.popitem()            # 最後の(k,v)を削除して返す（LIFO, Python 3.7+）
d.clear()              # 全削除

# setdefault — キーがなければ設定して返す ★
d = {}
d.setdefault("count", 0)    # 0（キーが存在しない→設定）
d["count"]                   # 0
d.setdefault("count", 99)   # 0（既存キー→変更しない）
```

### 5.3 辞書内包表記

```python
{x: x**2 for x in range(5)}
# {0: 0, 1: 1, 2: 4, 3: 9, 4: 16}

# キーと値の入れ替え
d = {"a": 1, "b": 2}
{v: k for k, v in d.items()}   # {1: "a", 2: "b"}

# フィルタ
{k: v for k, v in d.items() if v > 1}
```

### 5.4 collectionsの辞書型

```python
from collections import defaultdict, Counter, OrderedDict

# defaultdict — 存在しないキーにデフォルト値を自動設定
dd = defaultdict(list)
dd["fruits"].append("apple")   # KeyErrorにならない
dd["fruits"]                   # ["apple"]

dd = defaultdict(int)
dd["count"] += 1               # 0 + 1 = 1

# Counter — 要素の出現回数カウント
c = Counter("abracadabra")
c.most_common(3)    # [('a', 5), ('b', 2), ('r', 2)]
c["a"]              # 5
c + Counter("abc")  # Counter同士の加算

# OrderedDict — 挿入順保持（Python 3.7+ではdictも保持するが、等値比較が異なる）
od1 = OrderedDict([("a", 1), ("b", 2)])
od2 = OrderedDict([("b", 2), ("a", 1)])
od1 == od2          # False ★（順序も比較）

d1 = {"a": 1, "b": 2}
d2 = {"b": 2, "a": 1}
d1 == d2            # True（通常のdictは順序無関係）
```

### 5.5 辞書マージ（Python 3.9+）

```python
d1 = {"a": 1, "b": 2}
d2 = {"b": 3, "c": 4}

d1 | d2    # {"a": 1, "b": 3, "c": 4}（d2が優先）★
d2 | d1    # {"b": 2, "c": 4, "a": 1}（d1が優先）

# 破壊的マージ
d1 |= d2   # d1 = {"a": 1, "b": 3, "c": 4}
```

### 5.6 実務活用

```python
# JSONデータ操作
import json
data = json.loads('{"name": "Alice", "scores": [90, 85, 92]}')
avg = sum(data["scores"]) / len(data["scores"])

# グループ化集計
from collections import defaultdict
transactions = [("A", 100), ("B", 200), ("A", 150), ("B", 50)]
totals = defaultdict(int)
for name, amount in transactions:
    totals[name] += amount
# {'A': 250, 'B': 250}
```

---

## §6. 集合

### 6.1 基本

```python
# set — ミュータブル、要素はハッシュ可能かつユニーク
s = {1, 2, 3, 2, 1}   # {1, 2, 3}（重複排除）
s = set([1, 2, 3])     # リストから生成
s = set()              # 空集合 ★ {} は空辞書

# frozenset — イミュータブル（辞書キー・集合の要素に使える）
fs = frozenset([1, 2, 3])
```

### 6.2 集合演算 ★試験頻出

```python
a = {1, 2, 3, 4}
b = {3, 4, 5, 6}

# 和集合（どちらかに含まれる）
a | b                 # {1, 2, 3, 4, 5, 6}
a.union(b)

# 積集合（両方に含まれる）
a & b                 # {3, 4}
a.intersection(b)

# 差集合（aにあってbにない）
a - b                 # {1, 2}
a.difference(b)

# 対称差（どちらか一方にだけ含まれる）
a ^ b                 # {1, 2, 5, 6}
a.symmetric_difference(b)

# 部分集合・上位集合
{1, 2} <= {1, 2, 3}   # True（部分集合）
{1, 2}.issubset({1, 2, 3})
{1, 2, 3} >= {1, 2}   # True（上位集合）
{1, 2, 3}.issuperset({1, 2})
```

### 6.3 主要メソッド

```python
s = {1, 2, 3}
s.add(4)               # {1, 2, 3, 4}（1要素追加）
s.remove(4)            # {1, 2, 3}（なければKeyError）★
s.discard(99)          # 何もしない（なくてもエラーにならない）★
s.pop()                # 任意の1要素を削除して返す
s.clear()              # 全削除
```

### 6.4 実務活用

```python
# 重複排除
emails = ["a@x.com", "b@x.com", "a@x.com"]
unique = list(set(emails))   # 順序は保証されない

# 順序を保持した重複排除（Python 3.7+）
unique = list(dict.fromkeys(emails))

# 高速メンバーシップ判定 O(1)
valid_ids = {1001, 1002, 1003, 1004}
if user_id in valid_ids:   # O(1) ★ リストのO(n)より高速
    pass

# 差分検出
old_users = {"Alice", "Bob", "Charlie"}
new_users = {"Bob", "Charlie", "Dave"}
added = new_users - old_users    # {"Dave"}
removed = old_users - new_users  # {"Alice"}
```

---

## §7. 制御フロー

### 7.1 条件分岐

```python
# if/elif/else
x = 10
if x > 0:
    print("positive")
elif x == 0:
    print("zero")
else:
    print("negative")

# 三項演算子（条件式）
result = "even" if x % 2 == 0 else "odd"

# 連鎖比較 ★Python独自
1 < x < 100            # True（1 < x and x < 100 と同等）
```

### 7.2 ループ

```python
# for文
for i in range(5):     # 0, 1, 2, 3, 4
    print(i)

for i, v in enumerate(["a", "b", "c"]):   # インデックス付き
    print(i, v)        # 0 a, 1 b, 2 c

for k, v in {"a": 1}.items():   # 辞書イテレーション
    print(k, v)

# while文
while condition:
    pass

# break/continue
for i in range(10):
    if i == 3:
        continue       # 3をスキップ
    if i == 7:
        break          # 7で終了
    print(i)           # 0, 1, 2, 4, 5, 6
```

### 7.3 for/while の else節 ★試験頻出

```python
# elseブロック: ループがbreakされずに正常完了した場合に実行
for i in range(10):
    if i == 5:
        break
else:
    print("完了")      # breakされたので実行されない

for i in range(3):
    pass
else:
    print("完了")      # breakなしで完了 → 実行される ★

# 実用: 検索パターン
for item in items:
    if item == target:
        print("Found!")
        break
else:
    print("Not found")   # breakされなかった = 見つからなかった
```

### 7.4 match-case（Python 3.10+）

```python
# 構造的パターンマッチング
def handle_command(command):
    match command.split():
        case ["quit"]:
            return "Goodbye"
        case ["hello", name]:
            return f"Hello, {name}!"
        case ["add", *nums]:
            return sum(int(n) for n in nums)
        case _:                    # ワイルドカード（デフォルト）
            return "Unknown command"

# 型と構造のマッチ
match point:
    case (0, 0):
        print("Origin")
    case (x, 0):
        print(f"X-axis at {x}")
    case (0, y):
        print(f"Y-axis at {y}")
    case (x, y) if x == y:       # ガード条件
        print(f"Diagonal at {x}")
    case (x, y):
        print(f"Point({x}, {y})")
```

### 7.5 実務活用

```python
# パターンマッチによるJSONパース
match event:
    case {"type": "click", "element": elem}:
        handle_click(elem)
    case {"type": "scroll", "direction": d, "amount": a}:
        handle_scroll(d, a)
    case {"type": str() as t}:
        log(f"Unknown event: {t}")
```

---

## §8. 関数

### 8.1 関数定義

```python
def greet(name: str, greeting: str = "Hello") -> str:
    """挨拶文を返す。

    Args:
        name: 名前
        greeting: 挨拶の言葉

    Returns:
        挨拶文字列
    """
    return f"{greeting}, {name}!"
```

### 8.2 引数の種類 ★試験頻出

```python
# 位置引数
def f(a, b, c): ...
f(1, 2, 3)

# キーワード引数
f(a=1, c=3, b=2)

# デフォルト引数
def f(a, b=10): ...

# デフォルト引数のミュータブル問題 ★★★超頻出
def bad(lst=[]):          # ★リストはデフォルト引数に使うな
    lst.append(1)
    return lst
bad()    # [1]
bad()    # [1, 1] ★同じリストが使い回される

def good(lst=None):       # 正しいパターン
    if lst is None:
        lst = []
    lst.append(1)
    return lst

# 可変長位置引数 *args
def f(*args):
    print(args)           # タプルとして受け取る
f(1, 2, 3)               # (1, 2, 3)

# 可変長キーワード引数 **kwargs
def f(**kwargs):
    print(kwargs)         # 辞書として受け取る
f(a=1, b=2)              # {'a': 1, 'b': 2}

# 引数順序 ★
def f(pos, /, normal, *, kw_only, **kwargs):
    pass
# pos: 位置専用（/の前）
# normal: 位置でもキーワードでもOK
# kw_only: キーワード専用（*の後）

# アンパック呼び出し
args = [1, 2, 3]
f(*args)                  # f(1, 2, 3)
kwargs = {"a": 1, "b": 2}
f(**kwargs)               # f(a=1, b=2)
```

### 8.3 lambda式

```python
# 無名関数（式を1つだけ含む）
square = lambda x: x ** 2
add = lambda x, y: x + y

# sorted/map/filterとの組み合わせ
sorted(data, key=lambda x: x["age"])
list(map(lambda x: x * 2, [1, 2, 3]))
list(filter(lambda x: x > 0, [-1, 0, 1, 2]))
```

### 8.4 クロージャとnonlocal

```python
def counter():
    count = 0
    def increment():
        nonlocal count     # 外側スコープの変数を変更 ★
        count += 1
        return count
    return increment

c = counter()
c()    # 1
c()    # 2
c()    # 3
```

### 8.5 デコレータ ★試験頻出

```python
import functools
import time

# 基本デコレータ
def timer(func):
    @functools.wraps(func)    # ★元関数の__name__等を保持
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        elapsed = time.time() - start
        print(f"{func.__name__}: {elapsed:.3f}s")
        return result
    return wrapper

@timer
def slow_function():
    time.sleep(1)

# 引数付きデコレータ
def repeat(n):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for _ in range(n):
                result = func(*args, **kwargs)
            return result
        return wrapper
    return decorator

@repeat(3)
def greet():
    print("Hello")
```

### 8.6 ジェネレータ ★試験頻出

```python
# yield で値を逐次返す（メモリ効率的）
def fibonacci():
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b

gen = fibonacci()
next(gen)    # 0
next(gen)    # 1
next(gen)    # 1

# ジェネレータ式
g = (x ** 2 for x in range(1000000))   # メモリを消費しない

# yield from — サブジェネレータに委譲
def chain(*iterables):
    for it in iterables:
        yield from it

list(chain([1, 2], [3, 4]))   # [1, 2, 3, 4]

# send — ジェネレータに値を送る
def accumulator():
    total = 0
    while True:
        value = yield total
        total += value

acc = accumulator()
next(acc)           # 0（初回はnext()で起動）
acc.send(10)        # 10
acc.send(20)        # 30
```

### 8.7 イテレータプロトコル

```python
# __iter__と__next__を実装
class CountDown:
    def __init__(self, start):
        self.current = start

    def __iter__(self):
        return self

    def __next__(self):
        if self.current <= 0:
            raise StopIteration
        self.current -= 1
        return self.current + 1

for i in CountDown(3):
    print(i)          # 3, 2, 1
```

### 8.8 実務活用

```python
# デコレータによるキャッシュ
from functools import lru_cache

@lru_cache(maxsize=128)
def expensive_query(user_id):
    return db.query(user_id)

# デコレータによる認証
def require_auth(func):
    @functools.wraps(func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            raise PermissionError("Unauthorized")
        return func(request, *args, **kwargs)
    return wrapper

# ジェネレータによる大量データ処理
def read_large_file(path):
    with open(path) as f:
        for line in f:
            yield line.strip()
```

---

## §9. スコープとネームスペース

### 9.1 LEGB規則 ★試験頻出

```
L: Local      — 関数内のローカル変数
E: Enclosing  — 外側の関数（クロージャ）のローカル変数
G: Global     — モジュールレベルの変数
B: Built-in   — 組み込み名前空間（print, len等）
```

```python
x = "global"

def outer():
    x = "enclosing"

    def inner():
        x = "local"
        print(x)       # "local" (L)

    inner()
    print(x)           # "enclosing" (E)

outer()
print(x)               # "global" (G)
```

### 9.2 global文とnonlocal文

```python
x = 10

def modify_global():
    global x           # グローバル変数を変更可能にする
    x = 20

def outer():
    y = 10
    def inner():
        nonlocal y     # 外側関数の変数を変更可能にする
        y = 20
    inner()
    print(y)           # 20

# globalなしで代入するとローカル変数が作られる ★
x = 10
def f():
    x = 20             # ローカル変数xが作られる（グローバルxは変わらない）
f()
print(x)               # 10

# UnboundLocalError ★試験頻出
x = 10
def f():
    print(x)           # UnboundLocalError ★
    x = 20             # この代入があるためxはローカルと判断される
```

### 9.3 __name__パターン

```python
# モジュールとして直接実行された場合のみ実行
if __name__ == "__main__":
    main()

# importされた場合: __name__ == モジュール名
# 直接実行された場合: __name__ == "__main__"
```

### 9.4 実務活用

```python
# グローバル状態を避ける設計
class AppConfig:
    _instance = None

    @classmethod
    def get(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

# モジュールレベルの定数は UPPER_CASE で定義
MAX_RETRIES = 3
DEFAULT_TIMEOUT = 30
```

---

## §10. 型ヒント

### 10.1 基本型ヒント

```python
# 変数
name: str = "Alice"
age: int = 30
scores: list[int] = [90, 85, 92]
config: dict[str, int] = {"timeout": 30}

# 関数
def greet(name: str) -> str:
    return f"Hello, {name}"

# Optional（Noneを許容）
from typing import Optional
def find(key: str) -> Optional[str]:   # str | None と同等
    ...

# Union（複数型）
from typing import Union
def process(data: Union[str, bytes]) -> str:
    ...

# Python 3.10+: X | Y 構文
def process(data: str | bytes) -> str:
    ...
```

### 10.2 typingモジュール

```python
from typing import (
    TypeVar, Generic, Protocol, TypedDict,
    Literal, Final, ClassVar, Callable, Any
)

# TypeVar（ジェネリクス）
T = TypeVar("T")
def first(lst: list[T]) -> T:
    return lst[0]

# Generic
class Stack(Generic[T]):
    def __init__(self) -> None:
        self._items: list[T] = []
    def push(self, item: T) -> None:
        self._items.append(item)
    def pop(self) -> T:
        return self._items.pop()

# Protocol（構造的部分型）
class Drawable(Protocol):
    def draw(self) -> None: ...

# TypedDict（辞書の型定義）
class UserDict(TypedDict):
    name: str
    age: int
    email: str

# Literal（許可される値の限定）
def set_mode(mode: Literal["read", "write"]) -> None: ...

# Callable（関数型）
def apply(func: Callable[[int, int], int], a: int, b: int) -> int:
    return func(a, b)

# Final（再代入禁止）
MAX_SIZE: Final = 100
```

### 10.3 実務活用

```python
# mypy/pyrightによる静的型検査
# mypy example.py --strict

# 型ガード
from typing import TypeGuard

def is_str_list(val: list[object]) -> TypeGuard[list[str]]:
    return all(isinstance(x, str) for x in val)

# 実行時には型ヒントは無視される（ドキュメントと静的解析用）
# 実行時に型チェックしたい場合は isinstance() を使う
```
