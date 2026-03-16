# オブジェクト指向・例外処理 — Python3リファレンス

> Python 3 エンジニア認定基礎試験 満点レベル対応

---

## §1. クラスの基本

### 1.1 クラス定義

```python
class Dog:
    # クラス変数（全インスタンスで共有）
    species = "Canis familiaris"
    count = 0

    def __init__(self, name: str, age: int):
        # インスタンス変数（各インスタンス固有）
        self.name = name
        self.age = age
        Dog.count += 1

    def bark(self) -> str:
        """インスタンスメソッド"""
        return f"{self.name} says Woof!"

    @classmethod
    def from_string(cls, data: str) -> "Dog":
        """クラスメソッド — クラス自体を受け取る"""
        name, age = data.split(",")
        return cls(name, int(age))

    @staticmethod
    def is_valid_age(age: int) -> bool:
        """静的メソッド — self/clsを受け取らない"""
        return 0 <= age <= 30

dog = Dog("Rex", 5)
dog.bark()                       # "Rex says Woof!"
Dog.from_string("Max,3")         # クラスメソッドで生成
Dog.is_valid_age(25)             # True
```

### 1.2 インスタンス変数 vs クラス変数 ★試験頻出

```python
class Counter:
    total = 0                    # クラス変数

    def __init__(self):
        Counter.total += 1       # クラス変数はクラス名で参照 ★
        self.id = Counter.total  # インスタンス変数

# ★注意: self.total = ... とするとインスタンス変数が新しく作られる
# クラス変数を変更するには Counter.total を使う

class Trap:
    items = []                   # ★ミュータブルなクラス変数は共有される

    def add(self, item):
        self.items.append(item)  # 全インスタンスで同じリスト!

t1 = Trap()
t2 = Trap()
t1.add("a")
print(t2.items)                  # ["a"] ★全インスタンスに影響

# 正しくはインスタンス変数にする
class Safe:
    def __init__(self):
        self.items = []          # インスタンスごとに独立
```

### 1.3 プロパティ ★

```python
class Temperature:
    def __init__(self, celsius: float):
        self._celsius = celsius

    @property
    def celsius(self) -> float:
        """getter"""
        return self._celsius

    @celsius.setter
    def celsius(self, value: float):
        """setter — バリデーション可能"""
        if value < -273.15:
            raise ValueError("Absolute zero violation")
        self._celsius = value

    @celsius.deleter
    def celsius(self):
        """deleter"""
        del self._celsius

    @property
    def fahrenheit(self) -> float:
        """読み取り専用プロパティ（setterなし）"""
        return self._celsius * 9/5 + 32

t = Temperature(100)
t.celsius                # 100（getterが呼ばれる）
t.celsius = 200          # setterが呼ばれる
t.fahrenheit             # 392.0
t.fahrenheit = 100       # AttributeError（setter未定義）★
```

### 1.4 __slots__

```python
# __slots__ — 属性を固定してメモリを節約
class Point:
    __slots__ = ("x", "y")       # 許可する属性名を明示

    def __init__(self, x, y):
        self.x = x
        self.y = y

p = Point(1, 2)
p.z = 3                         # AttributeError ★（__slots__にない属性は追加不可）

# __slots__の効果
# 1. __dict__が作られない → メモリ削減（大量インスタンス時に有効）
# 2. 属性アクセスがやや高速
# 3. 動的な属性追加を防止
```

### 1.5 アクセス制御規約

```python
class MyClass:
    def public_method(self):        # パブリック
        pass

    def _protected_method(self):    # 保護（規約のみ、アクセス制限なし）
        pass

    def __private_method(self):     # プライベート（名前マングリング）
        pass

obj = MyClass()
obj.public_method()              # OK
obj._protected_method()         # OK（アクセス可能だが非推奨）
obj.__private_method()          # AttributeError
obj._MyClass__private_method()  # OK ★（名前マングリング: _クラス名__メソッド名）
```

### 1.6 実務活用

```python
# バリデーション付きデータモデル
class User:
    __slots__ = ("_name", "_email")

    def __init__(self, name: str, email: str):
        self.name = name     # setter経由
        self.email = email

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str):
        if not value.strip():
            raise ValueError("Name cannot be empty")
        self._name = value.strip()

    @property
    def email(self) -> str:
        return self._email

    @email.setter
    def email(self, value: str):
        if "@" not in value:
            raise ValueError("Invalid email")
        self._email = value.lower()

# ファクトリメソッド
class Connection:
    @classmethod
    def from_url(cls, url: str) -> "Connection":
        parsed = urlparse(url)
        return cls(host=parsed.hostname, port=parsed.port)

    @classmethod
    def from_config(cls, config: dict) -> "Connection":
        return cls(**config)
```

---

## §2. 継承

### 2.1 単一継承

```python
class Animal:
    def __init__(self, name: str):
        self.name = name

    def speak(self) -> str:
        raise NotImplementedError

class Dog(Animal):
    def speak(self) -> str:
        return f"{self.name}: Woof!"

class Cat(Animal):
    def __init__(self, name: str, indoor: bool = True):
        super().__init__(name)    # 親クラスの__init__を呼ぶ ★
        self.indoor = indoor

    def speak(self) -> str:
        return f"{self.name}: Meow!"

# isinstance / issubclass
dog = Dog("Rex")
isinstance(dog, Dog)       # True
isinstance(dog, Animal)    # True ★（親クラスもTrue）
issubclass(Dog, Animal)    # True
```

### 2.2 super() ★試験頻出

```python
class Base:
    def __init__(self):
        print("Base.__init__")

class Child(Base):
    def __init__(self):
        super().__init__()       # 親クラスの__init__を呼ぶ
        print("Child.__init__")

# super()はMROに従って次のクラスを呼ぶ（必ずしも直接の親とは限らない）★
```

### 2.3 多重継承とMRO ★★★試験頻出

```python
class A:
    def method(self):
        return "A"

class B(A):
    def method(self):
        return "B"

class C(A):
    def method(self):
        return "C"

class D(B, C):
    pass

D().method()         # "B" ★
D.__mro__            # (D, B, C, A, object)

# MRO（Method Resolution Order）— C3線形化アルゴリズム
# 1. 自分自身
# 2. 左から右の順に親クラスを深さ優先で検索
# 3. 同じクラスが複数回出る場合、最後の出現以外を削除

# ダイヤモンド継承
#     A
#    / \
#   B   C
#    \ /
#     D
# MRO: D → B → C → A → object
```

### 2.4 ミックスイン

```python
# 機能を追加するための小さなクラス（単体では使わない）
class JsonMixin:
    def to_json(self) -> str:
        import json
        return json.dumps(self.__dict__)

class LogMixin:
    def log(self, message: str):
        print(f"[{self.__class__.__name__}] {message}")

class User(JsonMixin, LogMixin):
    def __init__(self, name: str):
        self.name = name

u = User("Alice")
u.to_json()          # '{"name": "Alice"}'
u.log("created")     # [User] created
```

### 2.5 ABC（抽象基底クラス）★

```python
from abc import ABC, abstractmethod

class Shape(ABC):
    @abstractmethod
    def area(self) -> float:
        """面積を返す（サブクラスで実装必須）"""
        pass

    @abstractmethod
    def perimeter(self) -> float:
        pass

    def description(self) -> str:
        """具象メソッド（オーバーライド任意）"""
        return f"{self.__class__.__name__}: area={self.area():.2f}"

# Shape()          # TypeError: 抽象クラスはインスタンス化不可 ★

class Circle(Shape):
    def __init__(self, radius: float):
        self.radius = radius

    def area(self) -> float:
        import math
        return math.pi * self.radius ** 2

    def perimeter(self) -> float:
        import math
        return 2 * math.pi * self.radius

# 抽象メソッドをすべて実装しないとインスタンス化不可 ★
class Incomplete(Shape):
    def area(self) -> float:
        return 0
# Incomplete()     # TypeError: perimeter未実装
```

### 2.6 実務活用

```python
# プラグインアーキテクチャ
class Plugin(ABC):
    @abstractmethod
    def process(self, data: dict) -> dict:
        pass

    @classmethod
    def register(cls):
        """プラグイン登録（デコレータとして使用）"""
        registry.append(cls)
        return cls

# フレームワーク拡張
class BaseHandler(ABC):
    @abstractmethod
    def handle(self, request):
        pass

    def before_handle(self, request):
        pass  # フック（オーバーライド任意）

    def after_handle(self, request, response):
        pass  # フック（オーバーライド任意）

    def execute(self, request):
        self.before_handle(request)
        response = self.handle(request)
        self.after_handle(request, response)
        return response
```

---

## §3. 特殊メソッド（ダンダーメソッド）

### 3.1 文字列表現 ★試験頻出

```python
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self) -> str:
        """開発者向け表現（再現可能な文字列を推奨）"""
        return f"Point({self.x}, {self.y})"

    def __str__(self) -> str:
        """ユーザー向け表現"""
        return f"({self.x}, {self.y})"

p = Point(3, 4)
repr(p)          # "Point(3, 4)" — __repr__
str(p)           # "(3, 4)"      — __str__
print(p)         # "(3, 4)"      — __str__（なければ__repr__にフォールバック）★
f"{p}"           # "(3, 4)"      — __str__
f"{p!r}"         # "Point(3, 4)" — __repr__
```

### 3.2 比較

```python
class Student:
    def __init__(self, name, grade):
        self.name = name
        self.grade = grade

    def __eq__(self, other):
        if not isinstance(other, Student):
            return NotImplemented        # ★ False ではなく NotImplemented
        return self.grade == other.grade

    def __lt__(self, other):
        if not isinstance(other, Student):
            return NotImplemented
        return self.grade < other.grade

    def __le__(self, other):
        return self == other or self < other

    def __hash__(self):
        return hash(self.grade)    # __eq__を定義したら__hash__も定義 ★

# __eq__を定義すると__hash__はNoneになる（デフォルト）
# 辞書キーや集合要素にするには__hash__も必要
```

### 3.3 算術演算

```python
class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):        # self + other
        return Vector(self.x + other.x, self.y + other.y)

    def __radd__(self, other):       # other + self（otherが非Vector時）
        return self.__add__(other)

    def __mul__(self, scalar):       # self * scalar
        return Vector(self.x * scalar, self.y * scalar)

    def __rmul__(self, scalar):      # scalar * self
        return self.__mul__(scalar)

    def __neg__(self):               # -self
        return Vector(-self.x, -self.y)

    def __abs__(self):               # abs(self)
        return (self.x ** 2 + self.y ** 2) ** 0.5

    def __bool__(self):              # bool(self)
        return self.x != 0 or self.y != 0

v1 = Vector(1, 2)
v2 = Vector(3, 4)
v3 = v1 + v2            # Vector(4, 6)
v4 = v1 * 3             # Vector(3, 6)
v5 = 3 * v1             # Vector(3, 6)（__rmul__）
abs(v2)                  # 5.0
```

### 3.4 コンテナプロトコル

```python
class Deck:
    def __init__(self):
        self._cards = list(range(52))

    def __len__(self):               # len(deck)
        return len(self._cards)

    def __getitem__(self, index):    # deck[0], deck[1:5]
        return self._cards[index]

    def __setitem__(self, index, value):  # deck[0] = x
        self._cards[index] = value

    def __delitem__(self, index):    # del deck[0]
        del self._cards[index]

    def __contains__(self, item):    # item in deck
        return item in self._cards

    def __iter__(self):              # for card in deck
        return iter(self._cards)

    def __reversed__(self):          # reversed(deck)
        return reversed(self._cards)

deck = Deck()
len(deck)                # 52
deck[0]                  # 0
51 in deck               # True
for card in deck:        # イテレーション可能
    pass
```

### 3.5 コンテキストマネージャ ★試験頻出

```python
class FileManager:
    def __init__(self, filename, mode):
        self.filename = filename
        self.mode = mode

    def __enter__(self):
        """with文の開始時に呼ばれる"""
        self.file = open(self.filename, self.mode)
        return self.file             # as 変数に代入される

    def __exit__(self, exc_type, exc_val, exc_tb):
        """with文の終了時に呼ばれる（例外発生時も）"""
        self.file.close()
        return False                 # True: 例外を握りつぶす ★
                                     # False: 例外を再送出

with FileManager("test.txt", "w") as f:
    f.write("Hello")

# contextlib — デコレータでコンテキストマネージャを作成
from contextlib import contextmanager

@contextmanager
def timer(label):
    import time
    start = time.time()
    yield                            # ★ ここでwithブロックが実行される
    elapsed = time.time() - start
    print(f"{label}: {elapsed:.3f}s")

with timer("processing"):
    heavy_computation()
```

### 3.6 呼び出し可能オブジェクト

```python
class Adder:
    def __init__(self, n):
        self.n = n

    def __call__(self, x):          # インスタンスを関数のように呼べる
        return self.n + x

add5 = Adder(5)
add5(3)              # 8
callable(add5)       # True
```

### 3.7 属性アクセス

```python
class DynamicAttrs:
    def __getattr__(self, name):
        """属性が見つからない場合に呼ばれる ★"""
        return f"<{name} not found>"

    def __setattr__(self, name, value):
        """属性設定時に常に呼ばれる"""
        super().__setattr__(name, value)

    def __delattr__(self, name):
        """属性削除時に呼ばれる"""
        super().__delattr__(name)

    # __getattribute__ — 全属性アクセスで常に呼ばれる（__getattr__より前）
    # 無限再帰に注意 ★
```

### 3.8 実務活用

```python
# カスタムコレクション
class LimitedList:
    def __init__(self, maxlen):
        self._data = []
        self._maxlen = maxlen

    def __len__(self):
        return len(self._data)

    def __getitem__(self, index):
        return self._data[index]

    def append(self, item):
        if len(self._data) >= self._maxlen:
            self._data.pop(0)
        self._data.append(item)

    def __repr__(self):
        return f"LimitedList({self._data}, maxlen={self._maxlen})"

# DSL的な設計
class Query:
    def __init__(self):
        self._filters = []

    def where(self, condition):
        self._filters.append(condition)
        return self           # メソッドチェーン

    def __iter__(self):
        return iter(self._apply_filters())
```

---

## §4. 例外処理

### 4.1 try/except/else/finally ★★★試験頻出

```python
try:
    result = 10 / x
except ZeroDivisionError:
    print("ゼロ除算")
except (TypeError, ValueError) as e:   # 複数例外をまとめてキャッチ
    print(f"型/値エラー: {e}")
except Exception as e:                 # その他の例外
    print(f"予期しないエラー: {e}")
else:
    print(f"成功: {result}")           # ★例外が発生しなかった場合のみ実行
finally:
    print("必ず実行")                   # ★例外の有無に関わらず実行

# 実行順序 ★
# 正常: try → else → finally
# 例外: try → except → finally
# ★ elseはexceptが実行されない場合のみ
```

### 4.2 例外階層 ★試験頻出

```
BaseException
├── SystemExit              # sys.exit()
├── KeyboardInterrupt       # Ctrl+C
├── GeneratorExit           # ジェネレータのclose()
└── Exception               # ★ 通常のexceptでキャッチされる
    ├── ArithmeticError
    │   ├── ZeroDivisionError
    │   └── OverflowError
    ├── LookupError
    │   ├── IndexError
    │   └── KeyError
    ├── ValueError
    ├── TypeError
    ├── AttributeError
    ├── FileNotFoundError    # OSError のサブクラス
    ├── PermissionError      # OSError のサブクラス
    ├── ImportError
    │   └── ModuleNotFoundError
    ├── RuntimeError
    │   └── RecursionError
    ├── StopIteration
    ├── NameError
    └── OSError (IOError)
```

```python
# ★ except Exception で KeyboardInterrupt/SystemExit はキャッチしない
# → Ctrl+C を握りつぶさない安全な設計

# ★ 広い例外を先にキャッチするとサブクラスがキャッチされない
try:
    pass
except Exception:        # ★すべてキャッチ（後のexceptに到達しない）
    pass
except ValueError:       # 到達不能 ★
    pass
```

### 4.3 raise

```python
# 例外の発生
raise ValueError("不正な値")
raise TypeError("型エラー")
raise RuntimeError        # 引数なしも可

# 例外の再送出
try:
    risky()
except Exception:
    logging.error("Error occurred")
    raise                  # ★ 元の例外をそのまま再送出

# 例外チェーン（raise ... from ...）
try:
    data = json.loads(raw)
except json.JSONDecodeError as e:
    raise ValueError("JSONパースエラー") from e  # ★ 原因の例外を保持

# 例外チェーンを抑制
raise ValueError("msg") from None
```

### 4.4 カスタム例外

```python
class AppError(Exception):
    """アプリケーション基底例外"""
    pass

class NotFoundError(AppError):
    """リソース未発見"""
    def __init__(self, resource: str, resource_id: int):
        self.resource = resource
        self.resource_id = resource_id
        super().__init__(f"{resource} #{resource_id} not found")

class ValidationError(AppError):
    """バリデーションエラー"""
    def __init__(self, field: str, message: str):
        self.field = field
        super().__init__(f"{field}: {message}")

# 使用
try:
    raise NotFoundError("User", 42)
except NotFoundError as e:
    print(e.resource, e.resource_id)   # "User", 42
except AppError as e:
    print("アプリエラー:", e)
```

### 4.5 warnings

```python
import warnings

# 警告の発行（プログラムは継続する）
warnings.warn("This is deprecated", DeprecationWarning)
warnings.warn("Performance issue", UserWarning)

# 警告の制御
warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("error", category=UserWarning)  # 例外にする

# コンテキストマネージャ
with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    deprecated_function()
```

### 4.6 実務活用

```python
# 堅牢なエラーハンドリング
import logging
logger = logging.getLogger(__name__)

def fetch_user(user_id: int) -> dict:
    try:
        response = api_client.get(f"/users/{user_id}")
        response.raise_for_status()
        return response.json()
    except ConnectionError:
        logger.error(f"Connection failed for user {user_id}")
        raise
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON for user {user_id}: {e}")
        raise AppError(f"Invalid response for user {user_id}") from e

# リトライパターン
def retry(func, max_attempts=3, delay=1.0):
    import time
    for attempt in range(max_attempts):
        try:
            return func()
        except Exception as e:
            if attempt == max_attempts - 1:
                raise
            logger.warning(f"Attempt {attempt+1} failed: {e}")
            time.sleep(delay * (2 ** attempt))  # 指数バックオフ

# EAFP（Easier to Ask Forgiveness than Permission）★Pythonicスタイル
# 悪い例（LBYL）
if "key" in d:
    value = d["key"]

# 良い例（EAFP）
try:
    value = d["key"]
except KeyError:
    value = default
```

---

## §5. メタプログラミング

### 5.1 デスクリプタプロトコル

```python
# デスクリプタ — 属性アクセスをカスタマイズ
class Validator:
    def __init__(self, min_value=None, max_value=None):
        self.min_value = min_value
        self.max_value = max_value

    def __set_name__(self, owner, name):
        self.name = name                    # 属性名を記録

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self                     # クラスからのアクセス
        return obj.__dict__.get(self.name)

    def __set__(self, obj, value):
        if self.min_value is not None and value < self.min_value:
            raise ValueError(f"{self.name}: {value} < {self.min_value}")
        if self.max_value is not None and value > self.max_value:
            raise ValueError(f"{self.name}: {value} > {self.max_value}")
        obj.__dict__[self.name] = value

    def __delete__(self, obj):
        del obj.__dict__[self.name]

class Product:
    price = Validator(min_value=0)
    quantity = Validator(min_value=0, max_value=10000)

    def __init__(self, name, price, quantity):
        self.name = name
        self.price = price           # Validator.__set__が呼ばれる
        self.quantity = quantity

p = Product("Widget", 9.99, 100)
p.price = -1                         # ValueError
```

### 5.2 メタクラス

```python
# type — すべてのクラスのメタクラス
type(int)        # <class 'type'>
type(type)       # <class 'type'>

# type()でクラスを動的生成
MyClass = type("MyClass", (object,), {"x": 10, "greet": lambda self: "hi"})

# カスタムメタクラス
class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]

class Database(metaclass=SingletonMeta):
    def __init__(self):
        self.connection = "connected"

db1 = Database()
db2 = Database()
db1 is db2               # True（同じインスタンス）

# __init_subclass__ — サブクラス作成時のフック（Python 3.6+）★
class Base:
    def __init_subclass__(cls, required_attr=None, **kwargs):
        super().__init_subclass__(**kwargs)
        if required_attr and not hasattr(cls, required_attr):
            raise TypeError(f"{cls.__name__} must define {required_attr}")

class Child(Base, required_attr="process"):
    def process(self):     # 定義しないとTypeError
        pass
```

### 5.3 デコレータクラス

```python
class retry:
    """リトライデコレータ（クラスベース）"""
    def __init__(self, max_attempts=3, exceptions=(Exception,)):
        self.max_attempts = max_attempts
        self.exceptions = exceptions

    def __call__(self, func):
        import functools
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(self.max_attempts):
                try:
                    return func(*args, **kwargs)
                except self.exceptions as e:
                    if attempt == self.max_attempts - 1:
                        raise
            return None
        return wrapper

@retry(max_attempts=5, exceptions=(ConnectionError, TimeoutError))
def fetch_data(url):
    pass
```

### 5.4 実務活用

```python
# ORMライクなフィールド定義
class Field:
    def __init__(self, field_type, required=True, default=None):
        self.field_type = field_type
        self.required = required
        self.default = default

    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        return obj.__dict__.get(self.name, self.default)

    def __set__(self, obj, value):
        if value is not None and not isinstance(value, self.field_type):
            raise TypeError(f"{self.name}: expected {self.field_type.__name__}")
        obj.__dict__[self.name] = value

class Model:
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        cls._fields = {
            k: v for k, v in cls.__dict__.items()
            if isinstance(v, Field)
        }

class User(Model):
    name = Field(str)
    age = Field(int, default=0)
    email = Field(str, required=False)

u = User()
u.name = "Alice"
u.age = "thirty"        # TypeError
```
