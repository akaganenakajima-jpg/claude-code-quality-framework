# ベストプラクティス・テスト — Python3リファレンス

> Python 3 エンジニア認定基礎試験 満点レベル対応

---

## §1. PEP 8 コーディングスタイル

### 1.1 インデント・行長

```python
# インデント: 4スペース（タブは非推奨）
def function():
    if True:
        pass

# 行長: コード79文字 / docstring・コメント72文字
# 長い行の折り返し
result = (first_variable
          + second_variable
          - third_variable)

# バックスラッシュ継続（括弧内が望ましい）
total = first + \
        second + \
        third
```

### 1.2 命名規則 ★試験頻出

| 対象 | スタイル | 例 |
|------|---------|-----|
| 変数・関数 | snake_case | `my_variable`, `calculate_total()` |
| クラス | PascalCase | `MyClass`, `HttpClient` |
| 定数 | UPPER_SNAKE | `MAX_RETRY`, `DEFAULT_TIMEOUT` |
| モジュール | snake_case | `my_module.py` |
| パッケージ | lowercase | `mypackage` |
| プライベート | _prefix | `_internal_method()` |
| 名前マングリング | __prefix | `__private_attr` |
| 特殊メソッド | __dunder__ | `__init__`, `__str__` |
| 使わない変数 | `_` | `for _ in range(10)` |

### 1.3 import順序 ★

```python
# 1. 標準ライブラリ
import os
import sys
from pathlib import Path

# 2. サードパーティ（空行で区切る）
import requests
import numpy as np

# 3. ローカル（空行で区切る）
from mypackage import utils
from .models import User

# import スタイル
import os                  # 推奨（明示的）
from os import path        # OK（特定のもの）
from os import *           # ★非推奨（名前空間汚染）
```

### 1.4 空行規則

```python
# トップレベルの関数・クラス定義: 2行空ける
def function_a():
    pass


def function_b():
    pass


class MyClass:
    # クラス内のメソッド: 1行空ける
    def method_a(self):
        pass

    def method_b(self):
        pass
```

### 1.5 その他のPEP 8規則

```python
# 比較
# 良い
if x is None:              # ★ None比較は is/is not
    pass
if not x:                  # 空チェック
    pass
if isinstance(x, int):     # 型チェック
    pass

# 悪い
if x == None:              # ★ == は使わない
    pass
if len(x) == 0:            # 冗長
    pass
if type(x) is int:         # isinstanceを使う
    pass

# スペース
# 良い
x = 1
d = {"key": "value"}
f(1, 2)
lst[1:3]

# 悪い
x=1
d = { "key" : "value" }
f (1 , 2)
lst [1 : 3]

# 代入式のスペース
# 良い
def f(x, y=10): pass
f(x, y=20)
# デフォルト引数・キーワード引数の=の前後にスペースなし ★
```

### 1.6 実務活用

```python
# PEP 8チェックツール
# flake8: pip install flake8 && flake8 mycode.py
# black: pip install black && black mycode.py（自動整形）
# isort: pip install isort && isort mycode.py（import整理）

# pyproject.toml での設定
# [tool.black]
# line-length = 88
#
# [tool.isort]
# profile = "black"
#
# [tool.flake8]
# max-line-length = 88
```

---

## §2. Pythonic なコード

### 2.1 EAFP vs LBYL ★試験頻出

```python
# LBYL (Look Before You Leap) — 事前チェック
if key in dictionary:
    value = dictionary[key]
else:
    value = default

# EAFP (Easier to Ask Forgiveness than Permission) — ★Pythonic
try:
    value = dictionary[key]
except KeyError:
    value = default

# さらにPythonic
value = dictionary.get(key, default)

# ファイル存在チェック
# LBYL（レースコンディションあり）
if os.path.exists(filename):
    with open(filename) as f:
        data = f.read()

# EAFP（Pythonic, レースコンディションなし）
try:
    with open(filename) as f:
        data = f.read()
except FileNotFoundError:
    data = ""
```

### 2.2 イディオム集 ★

```python
# スワップ
a, b = b, a

# enumerate
for i, item in enumerate(items):
    print(i, item)

# zip（並行イテレーション）
for name, score in zip(names, scores):
    print(name, score)

# 辞書のイテレーション
for key, value in d.items():
    print(key, value)

# 条件式（三項演算子）
x = "even" if n % 2 == 0 else "odd"

# 連鎖比較
if 0 < x < 100:
    pass

# 真偽値の直接利用
if items:          # if len(items) > 0 より Pythonic
    pass

if not name:       # if name == "" より Pythonic
    pass

# any / all
if any(x > 0 for x in numbers):
    pass

if all(isinstance(x, int) for x in data):
    pass

# 辞書のデフォルト値
count = d.get("key", 0)

# リスト内包表記 > map/filter
squares = [x**2 for x in range(10)]          # Pythonic
squares = list(map(lambda x: x**2, range(10)))  # 冗長

# joinによる文字列結合
result = ", ".join(items)       # Pythonic
result = ""
for item in items:              # 非効率
    result += item + ", "
```

### 2.3 walrus演算子 :=（Python 3.8+）

```python
# 代入と式を同時に行う
# 従来
line = input()
while line != "quit":
    process(line)
    line = input()

# walrus
while (line := input()) != "quit":
    process(line)

# リスト内包表記での活用
results = [
    y
    for x in data
    if (y := expensive(x)) > threshold
]

# 正規表現
import re
if m := re.search(r"\d+", text):
    print(m.group())
```

### 2.4 辞書マージ演算子（Python 3.9+）

```python
defaults = {"color": "red", "size": 10}
overrides = {"color": "blue", "weight": 5}

# Python 3.9+
merged = defaults | overrides   # {"color": "blue", "size": 10, "weight": 5}
defaults |= overrides           # 破壊的マージ

# Python 3.8以前
merged = {**defaults, **overrides}
```

### 2.5 構造的パターンマッチ（Python 3.10+, §7で詳述）

```python
match command:
    case {"action": "buy", "item": item, "quantity": int(qty)}:
        buy(item, qty)
    case {"action": "sell", "item": item}:
        sell(item)
    case _:
        error()
```

### 2.6 実務活用

```python
# コードレビューでの指摘パターン

# 指摘1: ループでの文字列結合
# Bad
result = ""
for s in strings:
    result += s + "\n"       # O(n^2)

# Good
result = "\n".join(strings)  # O(n)

# 指摘2: 不要なリスト化
# Bad
if len(list(filter(lambda x: x > 0, nums))) > 0:
    pass

# Good
if any(x > 0 for x in nums):
    pass

# 指摘3: 辞書の存在チェック+代入
# Bad
if key not in d:
    d[key] = []
d[key].append(value)

# Good
d.setdefault(key, []).append(value)

# Better
from collections import defaultdict
d = defaultdict(list)
d[key].append(value)
```

---

## §3. テスト

### 3.1 unittest ★試験頻出

```python
import unittest

class TestCalculator(unittest.TestCase):
    def setUp(self):
        """各テストメソッドの前に実行"""
        self.calc = Calculator()

    def tearDown(self):
        """各テストメソッドの後に実行"""
        pass

    @classmethod
    def setUpClass(cls):
        """テストクラス全体の前に1回実行"""
        pass

    @classmethod
    def tearDownClass(cls):
        """テストクラス全体の後に1回実行"""
        pass

    def test_add(self):
        self.assertEqual(self.calc.add(2, 3), 5)

    def test_divide_by_zero(self):
        with self.assertRaises(ZeroDivisionError):   # ★例外テスト
            self.calc.divide(1, 0)

    def test_approximate(self):
        self.assertAlmostEqual(0.1 + 0.2, 0.3, places=7)

    @unittest.skip("未実装")
    def test_future_feature(self):
        pass

    @unittest.skipIf(sys.platform == "win32", "Windows非対応")
    def test_unix_only(self):
        pass

# 主要assertメソッド
# assertEqual(a, b)         a == b
# assertNotEqual(a, b)      a != b
# assertTrue(x)             bool(x) is True
# assertFalse(x)            bool(x) is False
# assertIs(a, b)            a is b
# assertIsNone(x)           x is None
# assertIn(a, b)            a in b
# assertIsInstance(a, B)    isinstance(a, B)
# assertRaises(Exc)         例外発生を確認
# assertAlmostEqual(a, b)   浮動小数点の近似比較
# assertGreater(a, b)       a > b
# assertLess(a, b)          a < b
# assertRegex(s, r)         正規表現マッチ

# 実行
# python -m unittest test_module.py
# python -m unittest discover -s tests -p "test_*.py"
```

### 3.2 pytest ★推奨

```python
# テスト関数（クラス不要）
def test_add():
    assert add(2, 3) == 5

def test_divide_by_zero():
    import pytest
    with pytest.raises(ZeroDivisionError):
        divide(1, 0)

# fixture — テストの前準備
import pytest

@pytest.fixture
def sample_data():
    return [1, 2, 3, 4, 5]

@pytest.fixture
def db_connection():
    conn = create_connection()
    yield conn                   # ★ yieldの後がteardown
    conn.close()

def test_sum(sample_data):      # fixture名を引数に指定
    assert sum(sample_data) == 15

# パラメータ化テスト ★
@pytest.mark.parametrize("input,expected", [
    (1, 1),
    (2, 4),
    (3, 9),
    (-1, 1),
])
def test_square(input, expected):
    assert square(input) == expected

# conftest.py — 共有fixture（テストディレクトリに配置）
# conftest.py
@pytest.fixture(scope="session")
def app():
    return create_app(testing=True)

# マーカー
@pytest.mark.slow
def test_heavy():
    pass

# 実行: pytest -v tests/ -m "not slow"

# 一時ディレクトリ
def test_file_output(tmp_path):
    output = tmp_path / "result.txt"
    output.write_text("hello")
    assert output.read_text() == "hello"
```

### 3.3 mock ★

```python
from unittest.mock import patch, MagicMock, call

# patch — 対象をモックに置き換え
@patch("mymodule.requests.get")
def test_fetch(mock_get):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {"name": "Alice"}

    result = fetch_user(1)
    assert result["name"] == "Alice"
    mock_get.assert_called_once_with("https://api.example.com/users/1")

# MagicMock — 汎用モック
mock = MagicMock()
mock.method(1, 2, key="value")
mock.method.assert_called_with(1, 2, key="value")
mock.method.call_count      # 1

# side_effect — 動的な振る舞い
mock = MagicMock(side_effect=[1, 2, 3])
mock()    # 1
mock()    # 2
mock()    # 3

mock = MagicMock(side_effect=ValueError("error"))
# mock()  → ValueError

# コンテキストマネージャとして
with patch("mymodule.open", mock_open(read_data="file content")):
    result = read_config()
    assert result == "file content"

# patch.object
with patch.object(MyClass, "method", return_value=42):
    obj = MyClass()
    assert obj.method() == 42
```

### 3.4 doctest

```python
def add(a, b):
    """2つの数を足す。

    >>> add(2, 3)
    5
    >>> add(-1, 1)
    0
    >>> add(0.1, 0.2)  # doctest: +ELLIPSIS
    0.3000...
    """
    return a + b

# 実行
# python -m doctest mymodule.py
# python -m doctest mymodule.py -v
```

### 3.5 カバレッジ

```bash
# インストール
pip install coverage pytest-cov

# unittest
coverage run -m unittest discover
coverage report
coverage html          # HTMLレポート生成

# pytest
pytest --cov=mypackage --cov-report=html tests/
```

### 3.6 実務活用

```python
# TDDサイクル
# 1. RED: 失敗するテストを書く
def test_user_creation():
    user = User("Alice", "alice@example.com")
    assert user.name == "Alice"
    assert user.email == "alice@example.com"
    assert user.is_active is True

# 2. GREEN: テストを通す最小限の実装
class User:
    def __init__(self, name, email):
        self.name = name
        self.email = email
        self.is_active = True

# 3. REFACTOR: 改善（テストは変更しない）

# テスト構造
# tests/
# ├── conftest.py       # 共有fixture
# ├── test_models.py    # モデルテスト
# ├── test_api.py       # APIテスト
# └── test_utils.py     # ユーティリティテスト
```

---

## §4. パッケージ管理

### 4.1 pip と venv ★

```bash
# 仮想環境の作成・有効化
python -m venv .venv
source .venv/bin/activate       # Linux/Mac
.venv\Scripts\activate          # Windows

# パッケージのインストール
pip install requests
pip install requests==2.28.0    # バージョン指定
pip install "requests>=2.28"    # 最小バージョン
pip install -r requirements.txt

# requirements.txt の生成
pip freeze > requirements.txt

# パッケージ情報
pip list
pip show requests
pip install --upgrade requests
pip uninstall requests
```

### 4.2 pyproject.toml（PEP 621）★推奨

```toml
[build-system]
requires = ["setuptools>=68.0"]
build-backend = "setuptools.backends._legacy:_Backend"

[project]
name = "mypackage"
version = "1.0.0"
description = "My package description"
requires-python = ">=3.10"
dependencies = [
    "requests>=2.28",
    "click>=8.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.0",
    "black",
    "mypy",
]

[project.scripts]
mycommand = "mypackage.cli:main"
```

### 4.3 パッケージ構造

```
mypackage/
├── pyproject.toml
├── src/
│   └── mypackage/
│       ├── __init__.py        # パッケージ初期化
│       ├── core.py
│       ├── utils.py
│       └── subpackage/
│           ├── __init__.py
│           └── module.py
└── tests/
    ├── conftest.py
    └── test_core.py
```

### 4.4 __init__.py と import ★試験頻出

```python
# __init__.py — パッケージの初期化ファイル
# 空でもOK（パッケージとして認識させるために必要）★
# Python 3.3+: 暗黙的名前空間パッケージ（__init__.py不要だが推奨）

# __init__.py での公開API定義
# mypackage/__init__.py
from .core import MyClass
from .utils import helper

__all__ = ["MyClass", "helper"]   # from mypackage import * の対象

# 絶対import vs 相対import
from mypackage.core import MyClass    # 絶対import（推奨）
from .core import MyClass            # 相対import（パッケージ内のみ）
from ..utils import helper           # 親パッケージの相対import
```

### 4.5 wheel と sdist

```bash
# ビルド
pip install build
python -m build          # dist/ に .whl と .tar.gz が生成

# wheel: バイナリ配布形式（インストール高速、ビルド不要）
# sdist: ソース配布形式（ビルドが必要）

# ローカルインストール
pip install .            # pyproject.toml から
pip install -e .         # 開発モード（editable install）★
```

### 4.6 実務活用

```python
# プロジェクトテンプレート
# requirements-dev.txt
-r requirements.txt
pytest>=7.0
black
mypy
flake8

# Makefile
# install:
#     pip install -e .[dev]
# test:
#     pytest -v tests/
# lint:
#     flake8 src/ && mypy src/ && black --check src/
# format:
#     black src/ tests/ && isort src/ tests/
```

---

## §5. パフォーマンス

### 5.1 計算量 ★★★試験頻出

| 操作 | リスト | 辞書 | 集合 |
|------|--------|------|------|
| 要素アクセス `x[i]` | O(1) | O(1) | - |
| 検索 `x in` | O(n) | O(1) ★ | O(1) ★ |
| 追加（末尾） | O(1) | O(1) | O(1) |
| 挿入（先頭） | O(n) ★ | - | - |
| 削除（末尾） | O(1) | - | - |
| 削除（先頭） | O(n) ★ | - | - |
| 削除（キー指定） | O(n) | O(1) | O(1) |
| ソート | O(n log n) | - | - |
| 長さ `len()` | O(1) | O(1) | O(1) |
| コピー | O(n) | O(n) | O(n) |

```python
# deque: 両端操作 O(1)
from collections import deque
dq = deque()
dq.appendleft(x)    # O(1) ★（listは O(n)）
dq.popleft()         # O(1) ★（listは O(n)）

# 文字列結合
# Bad: O(n^2)
result = ""
for s in strings:
    result += s

# Good: O(n)
result = "".join(strings)
```

### 5.2 プロファイリング

```python
# timeit — 実行時間の計測
import timeit

# コマンドラインから
# python -m timeit "sum(range(1000))"

# コード内
t = timeit.timeit("sum(range(1000))", number=10000)
print(f"{t:.4f}s")

# cProfile — 関数レベルのプロファイリング
import cProfile
cProfile.run("main()")

# コマンドライン
# python -m cProfile -s cumulative script.py

# プロファイル結果の読み方
# ncalls:     呼び出し回数
# tottime:    関数自体の実行時間
# percall:    1回あたりの時間
# cumtime:    子関数含む累積時間
# filename:   ファイル名と行番号
```

### 5.3 ジェネレータ vs リスト ★

```python
# リスト — 全要素をメモリに保持
squares = [x**2 for x in range(1_000_000)]  # ~8MB

# ジェネレータ — 1要素ずつ生成（メモリ効率的）
squares = (x**2 for x in range(1_000_000))  # ~100B ★

# ジェネレータが適する場面
# 1. 大量データの逐次処理
# 2. 全要素を同時に必要としない場合
# 3. パイプライン処理

# ジェネレータが不適な場面
# 1. ランダムアクセスが必要（squares[500]）
# 2. 複数回イテレーションが必要
# 3. 長さを事前に知る必要がある

# range もジェネレータ的（メモリ効率的）
r = range(1_000_000_000)   # メモリほぼ使わない
999_999_999 in r            # O(1) ★
```

### 5.4 __slots__によるメモリ削減

```python
import sys

class Normal:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Slotted:
    __slots__ = ("x", "y")
    def __init__(self, x, y):
        self.x = x
        self.y = y

n = Normal(1, 2)
s = Slotted(1, 2)
sys.getsizeof(n.__dict__)   # 104 bytes（__dict__のサイズ）
# Slottedには__dict__がない → メモリ節約

# 100万インスタンスで数十MB〜の差が出る
```

### 5.5 最適化テクニック

```python
# ローカル変数アクセスはグローバルより高速
def fast_loop():
    local_range = range     # ローカルに束縛
    local_append = result.append
    for i in local_range(1000000):
        local_append(i)

# 辞書のキャッシュ
from functools import lru_cache

@lru_cache(maxsize=256)
def expensive(n):
    return sum(i**2 for i in range(n))

# 集合による高速検索
# Bad: O(n) × m回
valid = [1, 2, 3, 4, 5]
for item in data:
    if item in valid:       # O(n)
        process(item)

# Good: O(1) × m回
valid = {1, 2, 3, 4, 5}
for item in data:
    if item in valid:       # O(1) ★
        process(item)

# 不要なコピーを避ける
# Bad
def process(data):
    data = data.copy()      # 不要なコピー
    return [x * 2 for x in data]

# Good
def process(data):
    return [x * 2 for x in data]  # 元データを変更しない

# str.join vs +=
# ★文字列結合は常にjoinを使う
parts = []
for item in data:
    parts.append(str(item))
result = ",".join(parts)
```

### 5.6 実務活用

```python
# ボトルネック特定のワークフロー
# 1. cProfile で全体像を把握
# python -m cProfile -o profile.dat script.py
# python -m pstats profile.dat
# >>> sort cumulative
# >>> stats 20

# 2. timeit で個別計測
# python -m timeit -s "data = list(range(10000))" "sorted(data)"

# 3. メモリ計測
# pip install memory-profiler
# @profile
# def my_func():
#     ...
# python -m memory_profiler script.py

# パフォーマンス改善チェックリスト
# □ 適切なデータ構造を使っているか（list vs dict vs set）
# □ 不要なリスト化をしていないか（ジェネレータで十分か）
# □ ループ内で重い処理を繰り返していないか（キャッシュ可能か）
# □ 文字列結合に += を使っていないか（join推奨）
# □ 検索に list.in を使っていないか（set/dict推奨）
# □ 大量インスタンスに __slots__ を使っているか
# □ I/O束縛処理を並行化できないか（asyncio/threading）
# □ CPU束縛処理を並列化できないか（multiprocessing）
```
