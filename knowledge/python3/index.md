# Python 3 エンジニア認定基礎試験 — 知識ベース索引

> 満点レベル対応。Pythonチュートリアル（公式）準拠 + 実務活用パターン付き。

## ファイル構成

| # | ファイル | 内容 | 主要トピック数 |
|---|---------|------|---------------|
| 1 | `core-syntax.md` | コア構文・データ型 | 10 |
| 2 | `stdlib.md` | 標準ライブラリ | 8 |
| 3 | `oop.md` | オブジェクト指向・例外処理 | 5 |
| 4 | `best-practices.md` | ベストプラクティス・テスト | 5 |

## 横断マップ（トリガー → 参照先）

| トリガー（業務・キーワード） | 参照ファイル | セクション |
|---|---|---|
| 変数・型・数値・文字列・リスト・辞書・集合 | `core-syntax.md` | §1-§6 |
| if/for/while・制御フロー・match-case | `core-syntax.md` | §7 |
| 関数・引数・lambda・デコレータ・ジェネレータ | `core-syntax.md` | §8 |
| スコープ・LEGB・global・nonlocal | `core-syntax.md` | §9 |
| 型ヒント・typing・mypy | `core-syntax.md` | §10 |
| ファイル操作・open・pathlib・os | `stdlib.md` | §1 |
| collections・heapq・bisect・dataclass・enum | `stdlib.md` | §2 |
| itertools・functools・map・filter | `stdlib.md` | §3 |
| datetime・日付・時間・タイムゾーン | `stdlib.md` | §4 |
| JSON・CSV・XML・シリアライズ | `stdlib.md` | §5 |
| threading・multiprocessing・asyncio・GIL | `stdlib.md` | §6 |
| HTTP・ネットワーク・socket | `stdlib.md` | §7 |
| re・math・logging・random・sys・argparse | `stdlib.md` | §8 |
| クラス・__init__・property・slots | `oop.md` | §1 |
| 継承・super・MRO・ABC・抽象クラス | `oop.md` | §2 |
| ダンダーメソッド・特殊メソッド・演算子オーバーロード | `oop.md` | §3 |
| 例外処理・try/except・raise・カスタム例外 | `oop.md` | §4 |
| メタクラス・デスクリプタ・メタプログラミング | `oop.md` | §5 |
| PEP 8・コーディングスタイル・命名規則 | `best-practices.md` | §1 |
| Pythonic・EAFP・walrus・アンパッキング | `best-practices.md` | §2 |
| テスト・unittest・pytest・mock・TDD | `best-practices.md` | §3 |
| pip・venv・パッケージ・import | `best-practices.md` | §4 |
| パフォーマンス・プロファイリング・計算量 | `best-practices.md` | §5 |

## 試験範囲と出題比率（参考）

| 分野 | 出題比率 | 対応ファイル |
|---|---|---|
| データ型・変数 | ~15% | `core-syntax.md` §1-§6 |
| 制御フロー | ~10% | `core-syntax.md` §7 |
| 関数 | ~15% | `core-syntax.md` §8-§9 |
| 組み込み型の操作 | ~10% | `core-syntax.md` §3-§6 |
| モジュール・パッケージ | ~10% | `stdlib.md`, `best-practices.md` §4 |
| ファイル操作 | ~5% | `stdlib.md` §1 |
| クラス・OOP | ~15% | `oop.md` §1-§3 |
| 例外処理 | ~10% | `oop.md` §4 |
| 標準ライブラリ | ~10% | `stdlib.md` §2-§8 |

## 使い方

1. 業務キーワードから上記横断マップで参照先を特定
2. 該当ファイルのセクション番号（§）を直接参照
3. 各セクション末尾の「実務活用」で実践パターンを確認
4. 試験対策は出題比率の高い分野から優先的に学習
