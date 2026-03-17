# practices/ — 開発プラクティス索引

> **プロジェクト CLAUDE.md の指定が優先**。ここは汎用デフォルト。

## ファイル一覧

| ファイル | 内容 | 関連IPA知識 |
|---|---|---|
| `coding-style.md` | 命名・関数設計・エラー処理・ファイル構成 | `ipa/ap.md` §SOLID |
| `security.md` | 入力検証・認証認可・秘密管理・ログ・インシデント対応 | `ipa/ap.md` + `ipa/au.md` |
| `testing.md` | TDD手順・予測モデル検証・カバレッジ戦略 | `ipa/sm.md` §テスト管理 |
| `git-workflow.md` | ブランチ戦略・コミット規約・PR・ロールバック | `ipa/pm.md` §構成管理 |
| `dev-workflow.md` | 調査→計画→実装→レビュー（PDCA対応） | `quality/process.md` |

## 課題→ファイル逆引き

| やりたいこと | 参照ファイル |
|---|---|
| コードを書く・変える | `coding-style.md` → `security.md` → `testing.md` |
| バグを直す | `testing.md` §バグ修正手順 → `dev-workflow.md` |
| 新機能を追加する | `dev-workflow.md` → `coding-style.md` → `testing.md` |
| PRを出す・レビューする | `git-workflow.md` → `testing.md` §カバレッジ |
| リファクタリングする | `coding-style.md` → `testing.md` §回帰テスト → `git-workflow.md` |
| デプロイする | `git-workflow.md` §ロールバック → `security.md` §インシデント対応 |
| 予測モデルを作る | `testing.md` §予測モデル検証（TDDではない） |
