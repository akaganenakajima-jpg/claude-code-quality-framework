# 標準ライブラリ — Python3リファレンス

> Python 3 エンジニア認定基礎試験 満点レベル対応

---

## §1. ファイル操作

### 1.1 open() と with文 ★試験頻出

```python
# 基本 — with文でファイルを安全に開閉
with open("data.txt", "r", encoding="utf-8") as f:
    content = f.read()        # 全体読み込み

with open("data.txt", "r", encoding="utf-8") as f:
    lines = f.readlines()     # 行リスト ["line1\n", "line2\n", ...]

with open("data.txt", "r", encoding="utf-8") as f:
    for line in f:            # 1行ずつイテレーション（メモリ効率的）★
        print(line.strip())

with open("data.txt", "r", encoding="utf-8") as f:
    line = f.readline()       # 1行読み込み
```

### 1.2 ファイルモード

| モード | 意味 | 備考 |
|--------|------|------|
| `"r"` | 読み取り（デフォルト） | ファイルが存在しないとFileNotFoundError |
| `"w"` | 書き込み | 既存内容を破棄 ★ |
| `"a"` | 追記 | 末尾に追加 |
| `"x"` | 排他的作成 | ファイルが存在するとFileExistsError |
| `"b"` | バイナリモード | `"rb"`, `"wb"` のように併用 |
| `"+"` | 読み書き両方 | `"r+"`, `"w+"` |
| `"t"` | テキストモード（デフォルト） | `"rt"` と `"r"` は同じ |

```python
# 書き込み
with open("output.txt", "w", encoding="utf-8") as f:
    f.write("Hello\n")
    f.writelines(["line1\n", "line2\n"])

# バイナリ
with open("image.png", "rb") as f:
    data = f.read()

# テキストとバイナリの違い ★
# テキスト: str を扱う、改行変換あり（Windows: \r\n → \n）
# バイナリ: bytes を扱う、変換なし
```

### 1.3 pathlib.Path（推奨） ★

```python
from pathlib import Path

# パス操作
p = Path("/home/user/data")
p / "file.txt"              # /home/user/data/file.txt（/演算子で結合）
p.parent                    # /home/user
p.name                      # "data"
p.stem                      # "data"（拡張子なし）
p.suffix                    # ""（拡張子）

f = Path("report.tar.gz")
f.stem                      # "report.tar"
f.suffix                    # ".gz"
f.suffixes                  # [".tar", ".gz"]

# 存在確認
p.exists()
p.is_file()
p.is_dir()

# ディレクトリ操作
p.mkdir(parents=True, exist_ok=True)
list(p.iterdir())           # 直下のファイル/ディレクトリ
list(p.glob("*.txt"))       # パターンマッチ
list(p.rglob("*.py"))       # 再帰的パターンマッチ

# ファイル読み書き（簡易）
text = Path("data.txt").read_text(encoding="utf-8")
Path("output.txt").write_text("Hello", encoding="utf-8")
data = Path("image.png").read_bytes()

# 絶対パス・相対パス
p.resolve()                 # 絶対パス
p.relative_to("/home")      # user/data
Path.cwd()                  # カレントディレクトリ
Path.home()                 # ホームディレクトリ
```

### 1.4 os / shutil

```python
import os
import shutil

# os
os.getcwd()                 # カレントディレクトリ
os.listdir(".")             # ディレクトリ内容
os.makedirs("a/b/c", exist_ok=True)  # 再帰的作成
os.remove("file.txt")       # ファイル削除
os.rename("old", "new")     # リネーム
os.path.join("a", "b", "c") # パス結合（pathlib推奨）
os.path.exists("file.txt")
os.path.isfile("file.txt")
os.path.isdir("dir")
os.path.basename("/a/b/c.txt")  # "c.txt"
os.path.dirname("/a/b/c.txt")   # "/a/b"
os.path.splitext("file.txt")    # ("file", ".txt")
os.environ["HOME"]          # 環境変数

# shutil
shutil.copy("src", "dst")       # ファイルコピー
shutil.copy2("src", "dst")      # メタデータ付きコピー
shutil.copytree("src", "dst")   # ディレクトリごとコピー
shutil.rmtree("dir")            # ディレクトリ再帰削除
shutil.move("src", "dst")       # 移動
```

### 1.5 実務活用

```python
# 設定ファイル読み込み
from pathlib import Path
import json

config_path = Path.home() / ".config" / "app" / "settings.json"
if config_path.exists():
    config = json.loads(config_path.read_text(encoding="utf-8"))
else:
    config = {"debug": False}

# ログファイルのローテーション
log_dir = Path("logs")
for old_log in sorted(log_dir.glob("*.log"))[:-5]:  # 最新5つ以外削除
    old_log.unlink()
```

---

## §2. データ構造

### 2.1 collections

```python
from collections import deque, defaultdict, Counter, OrderedDict, ChainMap

# deque — 両端キュー（O(1)で両端の追加・削除）★
dq = deque([1, 2, 3])
dq.append(4)            # 右端に追加 → [1,2,3,4]
dq.appendleft(0)        # 左端に追加 → [0,1,2,3,4]
dq.pop()                # 右端から削除 → 4
dq.popleft()            # 左端から削除 → 0
dq.rotate(1)            # 右に回転 [1,2,3] → [3,1,2]
dq.rotate(-1)           # 左に回転 [3,1,2] → [1,2,3]

# maxlen指定で固定長キュー
dq = deque(maxlen=3)
dq.extend([1, 2, 3, 4])  # [2, 3, 4]（古い要素が自動削除）

# defaultdict — デフォルト値付き辞書（§5で既出）
dd = defaultdict(list)
dd["key"].append("value")

# Counter — カウンター（§5で既出）
c = Counter("mississippi")
c.most_common(2)         # [('s', 4), ('i', 4)]

# ChainMap — 複数辞書の論理的な統合
defaults = {"color": "red", "size": 10}
overrides = {"color": "blue"}
config = ChainMap(overrides, defaults)
config["color"]          # "blue"（前方優先）
config["size"]           # 10（defaultsにフォールバック）
```

### 2.2 heapq（ヒープキュー）

```python
import heapq

# 最小ヒープ（最小値が先頭）
data = [5, 3, 8, 1, 2]
heapq.heapify(data)          # [1, 2, 8, 5, 3]（ヒープ化、破壊的）
heapq.heappush(data, 0)      # 要素追加
heapq.heappop(data)          # 0（最小値を取り出す）

heapq.nlargest(3, data)      # 上位3件
heapq.nsmallest(3, data)     # 下位3件

# 最大ヒープは符号を反転して代用
heapq.heappush(heap, -value)
-heapq.heappop(heap)

# 優先度キュー
tasks = []
heapq.heappush(tasks, (1, "high priority"))
heapq.heappush(tasks, (3, "low priority"))
heapq.heappush(tasks, (2, "medium priority"))
heapq.heappop(tasks)         # (1, "high priority")
```

### 2.3 bisect（二分探索）

```python
import bisect

# ソート済みリストへの挿入位置を二分探索で求める
sorted_list = [1, 3, 5, 7, 9]
bisect.bisect_left(sorted_list, 5)     # 2（5の左側）
bisect.bisect_right(sorted_list, 5)    # 3（5の右側）★
bisect.insort(sorted_list, 4)          # [1, 3, 4, 5, 7, 9]（ソート済み挿入）
```

### 2.4 dataclasses ★

```python
from dataclasses import dataclass, field

@dataclass
class Point:
    x: float
    y: float
    z: float = 0.0                  # デフォルト値

@dataclass
class Config:
    name: str
    tags: list[str] = field(default_factory=list)  # ミュータブルはfactory ★
    _internal: int = field(init=False, default=0)   # __init__に含めない

    def __post_init__(self):
        self.name = self.name.upper()   # 初期化後の処理

# 自動生成: __init__, __repr__, __eq__
p1 = Point(1.0, 2.0)
p2 = Point(1.0, 2.0)
p1 == p2               # True（値で比較）

# frozen=True でイミュータブル
@dataclass(frozen=True)
class FrozenPoint:
    x: float
    y: float

# order=True で比較演算子を自動生成
@dataclass(order=True)
class Student:
    grade: float
    name: str
```

### 2.5 enum

```python
from enum import Enum, IntEnum, auto, Flag

class Color(Enum):
    RED = 1
    GREEN = 2
    BLUE = 3

Color.RED                # Color.RED
Color.RED.name           # "RED"
Color.RED.value          # 1
Color(1)                 # Color.RED
Color["RED"]             # Color.RED
list(Color)              # [Color.RED, Color.GREEN, Color.BLUE]

# auto()で自動番号割り当て
class Status(Enum):
    PENDING = auto()     # 1
    ACTIVE = auto()      # 2
    CLOSED = auto()      # 3

# IntEnum — int として比較可能
class Priority(IntEnum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3

Priority.HIGH > Priority.LOW   # True
Priority.HIGH + 1               # 4

# Flag — ビットフラグ
class Permission(Flag):
    READ = auto()
    WRITE = auto()
    EXECUTE = auto()

perm = Permission.READ | Permission.WRITE
Permission.READ in perm          # True
```

### 2.6 実務活用

```python
# deque で固定長バッファ（直近N件のログ保持）
from collections import deque
recent_logs = deque(maxlen=100)
recent_logs.append("2026-03-16 New event")

# Counter で頻度分析
from collections import Counter
words = text.lower().split()
top_words = Counter(words).most_common(10)

# dataclass で設定オブジェクト
@dataclass
class DBConfig:
    host: str = "localhost"
    port: int = 5432
    database: str = "mydb"
    pool_size: int = 10
```

---

## §3. イテレータ・関数型

### 3.1 itertools ★試験頻出

```python
import itertools

# 無限イテレータ
itertools.count(10, 2)          # 10, 12, 14, 16, ...
itertools.cycle("ABC")          # A, B, C, A, B, C, ...
itertools.repeat("X", 3)       # X, X, X

# 終端イテレータ
itertools.chain([1,2], [3,4])   # 1, 2, 3, 4（連結）
itertools.islice(range(100), 5, 10)  # 5, 6, 7, 8, 9（スライス）

itertools.accumulate([1,2,3,4])          # 1, 3, 6, 10（累積和）
itertools.accumulate([1,2,3,4], max)     # 1, 2, 3, 4（累積最大値）

# フィルタ
itertools.filterfalse(lambda x: x%2, range(10))  # 0,2,4,6,8
itertools.takewhile(lambda x: x<5, [1,3,6,2])    # 1, 3（条件不成立で終了）
itertools.dropwhile(lambda x: x<5, [1,3,6,2])    # 6, 2（条件不成立から開始）

# 組み合わせ
itertools.product("AB", "12")              # A1, A2, B1, B2（直積）
itertools.permutations("ABC", 2)           # AB, AC, BA, BC, CA, CB（順列）
itertools.combinations("ABCD", 2)          # AB, AC, AD, BC, BD, CD（組み合わせ）
itertools.combinations_with_replacement("AB", 2)  # AA, AB, BB（重複組み合わせ）

# グループ化
data = [("A", 1), ("A", 2), ("B", 3), ("B", 4)]
for key, group in itertools.groupby(data, key=lambda x: x[0]):
    print(key, list(group))
# A [('A',1), ('A',2)]
# B [('B',3), ('B',4)]
# ★ 事前にソートが必要（連続する同じキーをグループ化）

# starmap
itertools.starmap(pow, [(2,3), (3,2)])     # 8, 9
```

### 3.2 functools ★

```python
from functools import reduce, partial, lru_cache, cache, wraps, total_ordering

# reduce — 累積演算
reduce(lambda a, b: a + b, [1, 2, 3, 4])   # 10
reduce(lambda a, b: a * b, [1, 2, 3, 4])   # 24
reduce(lambda a, b: a + b, [1, 2, 3], 10)  # 16（初期値10）

# partial — 部分適用
from functools import partial
int_base2 = partial(int, base=2)
int_base2("1010")    # 10

# lru_cache — メモ化キャッシュ
@lru_cache(maxsize=128)
def fibonacci(n):
    if n < 2:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

fibonacci(100)    # 一瞬で計算

# cache — 無制限キャッシュ（Python 3.9+, lru_cache(maxsize=None)と同等）
@cache
def expensive(x):
    return x ** 2

# total_ordering — 比較メソッドを自動補完
@total_ordering
class Student:
    def __init__(self, grade):
        self.grade = grade
    def __eq__(self, other):
        return self.grade == other.grade
    def __lt__(self, other):
        return self.grade < other.grade
    # __le__, __gt__, __ge__ が自動生成される
```

### 3.3 組み込み関数型ツール

```python
# map — 各要素に関数を適用
list(map(str, [1, 2, 3]))           # ['1', '2', '3']
list(map(lambda x, y: x+y, [1,2], [3,4]))  # [4, 6]

# filter — 条件に合う要素を抽出
list(filter(None, [0, 1, "", "a"]))  # [1, "a"]（Truthyのみ）
list(filter(lambda x: x > 0, [-1, 0, 1, 2]))  # [1, 2]

# zip — 複数イテラブルを並行イテレーション
list(zip([1,2,3], ["a","b","c"]))    # [(1,'a'), (2,'b'), (3,'c')]
list(zip([1,2], [3,4,5]))           # [(1,3), (2,4)] ★短い方に合わせる

# zip_longest（itertools）
from itertools import zip_longest
list(zip_longest([1,2], [3,4,5], fillvalue=0))  # [(1,3),(2,4),(0,5)]

# enumerate — インデックス付きイテレーション
list(enumerate(["a", "b", "c"], start=1))
# [(1, 'a'), (2, 'b'), (3, 'c')]

# sorted, reversed, min, max, sum, any, all
any([False, False, True])    # True（1つでもTrue）
all([True, True, True])      # True（すべてTrue）
any([])                      # False ★
all([])                      # True  ★
```

### 3.4 operator

```python
from operator import itemgetter, attrgetter, methodcaller

# itemgetter — 辞書/タプルの要素取得関数を生成
data = [{"name": "Alice", "age": 30}, {"name": "Bob", "age": 25}]
sorted(data, key=itemgetter("age"))  # Bob(25), Alice(30)

# 複数キー
sorted(data, key=itemgetter("age", "name"))

# attrgetter — 属性取得
sorted(objects, key=attrgetter("name"))

# methodcaller — メソッド呼び出し
list(map(methodcaller("upper"), ["hello", "world"]))  # ["HELLO", "WORLD"]
```

### 3.5 実務活用

```python
# パイプライン的データ処理
from itertools import chain, islice
from functools import reduce

raw_data = [[1,2,3], [4,5,6], [7,8,9]]
result = sum(
    x ** 2
    for x in chain.from_iterable(raw_data)
    if x % 2 == 0
)  # 4 + 16 + 36 + 64 = 120

# 頻出パターン: 辞書リストの集計
from functools import reduce
orders = [{"total": 100}, {"total": 200}, {"total": 150}]
grand_total = reduce(lambda acc, o: acc + o["total"], orders, 0)  # 450
```

---

## §4. 日付・時間

### 4.1 datetime

```python
from datetime import date, time, datetime, timedelta

# date
d = date(2026, 3, 16)
d = date.today()
d.year, d.month, d.day     # (2026, 3, 16)
d.weekday()                 # 0=月曜 〜 6=日曜
d.isoweekday()              # 1=月曜 〜 7=日曜
d.isoformat()               # "2026-03-16"

# time
t = time(10, 30, 45)
t.hour, t.minute, t.second

# datetime
dt = datetime(2026, 3, 16, 10, 30, 45)
dt = datetime.now()
dt = datetime.utcnow()              # UTC（非推奨、timezone-aware推奨）
dt = datetime.now(tz=timezone.utc)   # UTC（推奨）
dt.date()                            # dateオブジェクト
dt.time()                            # timeオブジェクト

# timedelta — 時間差
delta = timedelta(days=7, hours=3, minutes=30)
tomorrow = date.today() + timedelta(days=1)
dt1 - dt2                            # timedelta オブジェクト
delta.total_seconds()                # 秒数に変換
```

### 4.2 フォーマット ★試験頻出

```python
# strftime — datetime → 文字列
dt.strftime("%Y-%m-%d %H:%M:%S")     # "2026-03-16 10:30:45"
dt.strftime("%Y年%m月%d日")           # "2026年03月16日"

# strptime — 文字列 → datetime
datetime.strptime("2026-03-16", "%Y-%m-%d")

# 主要フォーマットコード
# %Y: 4桁年   %m: 月(01-12)   %d: 日(01-31)
# %H: 時(00-23) %M: 分(00-59) %S: 秒(00-59)
# %A: 曜日名   %a: 曜日略称   %B: 月名   %b: 月略称
# %I: 12時間制 %p: AM/PM
# %j: 年内通算日 %U: 週番号(日曜始まり) %W: 週番号(月曜始まり)
```

### 4.3 タイムゾーン（Python 3.9+）

```python
from datetime import datetime, timezone
from zoneinfo import ZoneInfo

# UTC
utc_now = datetime.now(timezone.utc)

# タイムゾーン指定
jst = ZoneInfo("Asia/Tokyo")
jst_now = datetime.now(jst)

# 変換
utc_dt = jst_now.astimezone(timezone.utc)
```

### 4.4 実務活用

```python
# ログのタイムスタンプ処理
def parse_log_time(line):
    ts = line[:19]  # "2026-03-16 10:30:45"
    return datetime.strptime(ts, "%Y-%m-%d %H:%M:%S")

# 期間計算
def business_days(start, end):
    days = 0
    current = start
    while current <= end:
        if current.weekday() < 5:  # 月〜金
            days += 1
        current += timedelta(days=1)
    return days

# ISO 8601
dt.isoformat()  # "2026-03-16T10:30:45+09:00"
datetime.fromisoformat("2026-03-16T10:30:45+09:00")
```

---

## §5. JSON・CSV・XML

### 5.1 json ★試験頻出

```python
import json

# エンコード（Python → JSON文字列）
data = {"name": "太郎", "scores": [90, 85], "active": True, "address": None}
s = json.dumps(data)                          # コンパクト
s = json.dumps(data, ensure_ascii=False)       # 日本語そのまま ★
s = json.dumps(data, indent=2)                 # 整形
s = json.dumps(data, sort_keys=True)           # キーソート

# デコード（JSON文字列 → Python）
obj = json.loads('{"name": "Alice", "age": 30}')

# ファイル入出力
with open("data.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

with open("data.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# 型対応表 ★
# JSON     → Python
# object   → dict
# array    → list
# string   → str
# number   → int / float
# true     → True
# false    → False
# null     → None

# カスタムシリアライズ
from datetime import datetime
def default_handler(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()
    raise TypeError(f"Not serializable: {type(obj)}")

json.dumps({"time": datetime.now()}, default=default_handler)
```

### 5.2 csv

```python
import csv

# 読み込み
with open("data.csv", "r", encoding="utf-8") as f:
    reader = csv.reader(f)
    header = next(reader)     # ヘッダー行
    for row in reader:
        print(row)            # リスト ['value1', 'value2', ...]

# DictReader（ヘッダーをキーとして辞書で返す）★
with open("data.csv", "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        print(row["name"], row["age"])

# 書き込み
with open("output.csv", "w", encoding="utf-8", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["name", "age"])
    writer.writerows([["Alice", 30], ["Bob", 25]])

# DictWriter
with open("output.csv", "w", encoding="utf-8", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["name", "age"])
    writer.writeheader()
    writer.writerow({"name": "Alice", "age": 30})
```

### 5.3 xml.etree.ElementTree

```python
import xml.etree.ElementTree as ET

# パース
tree = ET.parse("data.xml")
root = tree.getroot()

# 走査
for child in root:
    print(child.tag, child.attrib, child.text)

root.findall(".//item")         # XPathで検索
root.find("./header/title").text

# 作成
root = ET.Element("root")
child = ET.SubElement(root, "item", attrib={"id": "1"})
child.text = "Hello"
tree = ET.ElementTree(root)
tree.write("output.xml", encoding="utf-8", xml_declaration=True)
```

### 5.4 実務活用

```python
# JSONレスポンスの処理
import json
response_text = '{"users": [{"name": "Alice"}, {"name": "Bob"}]}'
data = json.loads(response_text)
names = [u["name"] for u in data["users"]]

# CSVからの集計
import csv
from collections import Counter
with open("sales.csv") as f:
    reader = csv.DictReader(f)
    region_counts = Counter(row["region"] for row in reader)
```

---

## §6. 並行処理

### 6.1 threading ★

```python
import threading

# 基本
def worker(name):
    print(f"Thread {name} started")

t = threading.Thread(target=worker, args=("A",))
t.start()
t.join()          # スレッド完了を待つ

# Lock — 排他制御
lock = threading.Lock()
shared_counter = 0

def increment():
    global shared_counter
    with lock:                    # acquire/releaseの自動管理
        shared_counter += 1

# RLock — 再入可能ロック（同じスレッドが複数回取得可能）
rlock = threading.RLock()

# Event — スレッド間シグナル
event = threading.Event()
event.set()       # フラグをTrue
event.clear()     # フラグをFalse
event.wait()      # Trueになるまでブロック

# Semaphore — 同時アクセス数制限
sem = threading.Semaphore(3)   # 最大3スレッド同時
with sem:
    pass  # 処理

# GIL（Global Interpreter Lock）★★★
# CPythonではGILにより、同時に1スレッドしかPythonバイトコードを実行できない
# → CPU束縛処理ではマルチスレッドで高速化できない
# → I/O束縛処理ではGILが解放されるため効果あり
```

### 6.2 multiprocessing

```python
import multiprocessing

# 基本
def worker(x):
    return x ** 2

p = multiprocessing.Process(target=worker, args=(10,))
p.start()
p.join()

# Pool — プロセスプール
with multiprocessing.Pool(4) as pool:
    results = pool.map(worker, range(10))     # [0, 1, 4, 9, ...]
    results = pool.starmap(worker, [(1,), (2,), (3,)])

# Queue — プロセス間通信
q = multiprocessing.Queue()
q.put("data")
data = q.get()
```

### 6.3 concurrent.futures ★推奨

```python
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor, as_completed

# ThreadPoolExecutor（I/O束縛向け）
with ThreadPoolExecutor(max_workers=5) as executor:
    futures = [executor.submit(fetch_url, url) for url in urls]

    # 完了順に結果取得
    for future in as_completed(futures):
        try:
            result = future.result(timeout=10)
        except Exception as e:
            print(f"Error: {e}")

    # map（投入順に結果取得）
    results = list(executor.map(fetch_url, urls))

# ProcessPoolExecutor（CPU束縛向け）
with ProcessPoolExecutor(max_workers=4) as executor:
    results = list(executor.map(heavy_computation, data_list))
```

### 6.4 asyncio ★

```python
import asyncio

# コルーチン定義
async def fetch_data(url: str) -> str:
    await asyncio.sleep(1)     # 非同期スリープ
    return f"data from {url}"

# 複数タスクの並行実行
async def main():
    # gather — 全タスクの完了を待つ
    results = await asyncio.gather(
        fetch_data("url1"),
        fetch_data("url2"),
        fetch_data("url3"),
    )
    print(results)

    # Task の作成と管理
    task = asyncio.create_task(fetch_data("url4"))
    result = await task

    # タイムアウト
    try:
        result = await asyncio.wait_for(fetch_data("url5"), timeout=2.0)
    except asyncio.TimeoutError:
        print("Timed out")

# イベントループの実行
asyncio.run(main())

# async for（非同期イテレーション）
async def async_range(n):
    for i in range(n):
        await asyncio.sleep(0.1)
        yield i

async def main():
    async for i in async_range(5):
        print(i)

# async with（非同期コンテキストマネージャ）
async with aiohttp.ClientSession() as session:
    async with session.get(url) as response:
        data = await response.json()
```

### 6.5 GILと使い分け ★試験頻出

| 用途 | 推奨 | 理由 |
|------|------|------|
| CPU束縛 | multiprocessing / ProcessPoolExecutor | GIL回避 |
| I/O束縛（少数） | threading / ThreadPoolExecutor | シンプル |
| I/O束縛（大量） | asyncio | 軽量コルーチン |
| 混在 | ProcessPool + 各プロセス内でasyncio | 最大効率 |

### 6.6 実務活用

```python
# Web APIの並行呼び出し
import asyncio
import aiohttp

async def fetch_all(urls):
    async with aiohttp.ClientSession() as session:
        tasks = [session.get(url) for url in urls]
        responses = await asyncio.gather(*tasks)
        return [await r.json() for r in responses]

# CPU集約処理の並列化
from concurrent.futures import ProcessPoolExecutor

def analyze_file(path):
    # 重い処理
    return result

with ProcessPoolExecutor() as executor:
    results = list(executor.map(analyze_file, file_paths))
```

---

## §7. ネットワーク・HTTP

### 7.1 urllib

```python
from urllib.request import urlopen, Request
from urllib.parse import urlencode, urlparse, quote
import json

# GET
with urlopen("https://api.example.com/data") as response:
    data = json.loads(response.read().decode("utf-8"))
    print(response.status)       # 200
    print(response.headers)

# POST
data = urlencode({"key": "value"}).encode("utf-8")
req = Request("https://api.example.com/submit", data=data, method="POST")
req.add_header("Content-Type", "application/x-www-form-urlencoded")
with urlopen(req) as response:
    result = response.read()

# URL解析
parsed = urlparse("https://example.com:8080/path?key=value#section")
parsed.scheme    # "https"
parsed.hostname  # "example.com"
parsed.port      # 8080
parsed.path      # "/path"
parsed.query     # "key=value"

# URLエンコード
quote("日本語")  # "%E6%97%A5%E6%9C%AC%E8%AA%9E"
```

### 7.2 http.server

```python
# 簡易HTTPサーバ（デバッグ用）
# コマンドライン: python -m http.server 8000
from http.server import HTTPServer, SimpleHTTPRequestHandler
server = HTTPServer(("", 8000), SimpleHTTPRequestHandler)
server.serve_forever()
```

### 7.3 socket（基礎）

```python
import socket

# TCPクライアント
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect(("example.com", 80))
    s.sendall(b"GET / HTTP/1.1\r\nHost: example.com\r\n\r\n")
    data = s.recv(4096)

# UDPクライアント
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    s.sendto(b"Hello", ("localhost", 9999))
```

### 7.4 実務活用

```python
# REST API呼び出し（urllib）
import json
from urllib.request import Request, urlopen

def api_get(url, headers=None):
    req = Request(url, headers=headers or {})
    with urlopen(req, timeout=10) as resp:
        return json.loads(resp.read().decode("utf-8"))

def api_post(url, payload, headers=None):
    data = json.dumps(payload).encode("utf-8")
    h = {"Content-Type": "application/json"}
    h.update(headers or {})
    req = Request(url, data=data, headers=h, method="POST")
    with urlopen(req, timeout=10) as resp:
        return json.loads(resp.read().decode("utf-8"))
```

---

## §8. その他重要モジュール

### 8.1 math

```python
import math

math.ceil(3.2)        # 4（切り上げ）
math.floor(3.8)       # 3（切り捨て）
math.trunc(3.8)       # 3（ゼロ方向への切り捨て）★
math.trunc(-3.8)      # -3 （floorは-4）

math.sqrt(16)         # 4.0
math.log(100, 10)     # 2.0（底指定）
math.log2(8)          # 3.0
math.log10(1000)      # 3.0

math.gcd(12, 8)       # 4（最大公約数）
math.lcm(4, 6)        # 12（最小公倍数, Python 3.9+）
math.factorial(5)     # 120
math.comb(5, 2)       # 10（組み合わせ, Python 3.8+）
math.perm(5, 2)       # 20（順列, Python 3.8+）

math.isclose(0.1+0.2, 0.3)   # True ★
math.isinf(float("inf"))     # True
math.isnan(float("nan"))     # True

math.pi              # 3.141592653589793
math.e               # 2.718281828459045
math.inf             # float("inf")
math.nan             # float("nan")
```

### 8.2 statistics（Python 3.4+）

```python
import statistics

data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
statistics.mean(data)       # 5.5（算術平均）
statistics.median(data)     # 5.5（中央値）
statistics.mode([1,1,2,3])  # 1（最頻値）
statistics.stdev(data)      # 標準偏差（標本）
statistics.pstdev(data)     # 標準偏差（母集団）
statistics.variance(data)   # 分散（標本）
```

### 8.3 random

```python
import random

random.random()              # [0.0, 1.0) の浮動小数点
random.uniform(1.0, 10.0)   # [1.0, 10.0] の浮動小数点
random.randint(1, 6)         # [1, 6] の整数（両端含む）★
random.randrange(1, 7)       # [1, 7) の整数（range相当）
random.choice([1, 2, 3])    # ランダムに1要素選択
random.choices([1,2,3], k=5) # 重複あり複数選択
random.sample([1,2,3,4,5], k=3)  # 重複なし複数選択
random.shuffle(lst)          # リストをシャッフル（破壊的）
random.seed(42)              # シード固定（再現性）
```

### 8.4 sys

```python
import sys

sys.argv               # コマンドライン引数リスト ['script.py', 'arg1', ...]
sys.exit(0)            # プログラム終了（0: 正常, 非0: 異常）
sys.path               # モジュール検索パスリスト
sys.stdin              # 標準入力
sys.stdout             # 標準出力
sys.stderr             # 標準エラー出力
sys.version            # Pythonバージョン文字列
sys.platform           # プラットフォーム（'win32', 'linux', 'darwin'）
sys.getsizeof(obj)     # オブジェクトのメモリサイズ（バイト）
sys.maxsize            # プラットフォームのポインタが表現できる最大整数
sys.getrecursionlimit()  # 再帰上限（デフォルト1000）
sys.setrecursionlimit(n) # 再帰上限設定
```

### 8.5 logging ★

```python
import logging

# 基本設定
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

# ロガー取得
logger = logging.getLogger(__name__)

# ログレベル（低い→高い）★
# DEBUG < INFO < WARNING < ERROR < CRITICAL
logger.debug("詳細デバッグ情報")
logger.info("通常の動作情報")
logger.warning("警告（デフォルトレベル）")
logger.error("エラー発生")
logger.critical("致命的エラー")

# ハンドラ・フォーマッタ
handler = logging.FileHandler("app.log", encoding="utf-8")
handler.setLevel(logging.WARNING)
formatter = logging.Formatter("%(asctime)s %(levelname)s: %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)
```

### 8.6 argparse

```python
import argparse

parser = argparse.ArgumentParser(description="サンプルスクリプト")
parser.add_argument("input", help="入力ファイル")
parser.add_argument("-o", "--output", default="out.txt", help="出力ファイル")
parser.add_argument("-v", "--verbose", action="store_true", help="詳細表示")
parser.add_argument("-n", "--count", type=int, default=1, help="繰り返し回数")
parser.add_argument("--mode", choices=["fast", "slow"], default="fast")
args = parser.parse_args()

print(args.input, args.output, args.verbose, args.count)
```

### 8.7 unittest / pytest / pdb

```python
# unittest
import unittest

class TestMath(unittest.TestCase):
    def setUp(self):
        self.data = [1, 2, 3]

    def test_sum(self):
        self.assertEqual(sum(self.data), 6)

    def test_type(self):
        self.assertIsInstance(sum(self.data), int)

    def tearDown(self):
        pass

# pytest（簡潔なスタイル）
def test_sum():
    assert sum([1, 2, 3]) == 6

# pdb（デバッガ）
import pdb; pdb.set_trace()     # ブレークポイント
# Python 3.7+
breakpoint()                    # 同等
```

### 8.8 実務活用

```python
# ロギング設定のベストプラクティス
import logging
import sys

def setup_logging(level=logging.INFO):
    root = logging.getLogger()
    root.setLevel(level)

    console = logging.StreamHandler(sys.stdout)
    console.setFormatter(logging.Formatter(
        "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
    ))
    root.addHandler(console)

    file_handler = logging.FileHandler("app.log", encoding="utf-8")
    file_handler.setLevel(logging.WARNING)
    file_handler.setFormatter(logging.Formatter(
        "%(asctime)s [%(levelname)s] %(name)s (%(filename)s:%(lineno)d): %(message)s"
    ))
    root.addHandler(file_handler)

# argparse + logging の組み合わせ
parser = argparse.ArgumentParser()
parser.add_argument("--debug", action="store_true")
args = parser.parse_args()
setup_logging(logging.DEBUG if args.debug else logging.INFO)
```
