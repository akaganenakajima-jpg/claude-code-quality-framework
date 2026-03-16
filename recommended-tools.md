# 推奨ツール・MCP一覧

Claude Codeの品質管理フレームワークと連携して効果を発揮するツール群です。
全て任意ですが、「おすすめ」マークのツールは導入を推奨します。

## 前提条件

MCPサーバーの前提プログラムはMCPごとに異なります（Node.js / Python / Docker 等）。
**導入前に各MCPの公式ドキュメントで最新の要件を確認してください。**

一般的に必要なもの:

| 前提 | 確認コマンド | インストール |
|------|------------|-------------|
| Node.js | `node --version` | https://nodejs.org/ からLTSをインストール |
| Python | `python3 --version` | https://www.python.org/ からインストール |
| uv / uvx | `uvx --version` | https://docs.astral.sh/uv/getting-started/installation/ |

## おすすめ

### Notion MCP
- **できること**: Notionにドキュメントを自動記録・検索・更新
- **品質管理との関連**: 文書管理・記録保持（ISO9001 §7.5）
- **追加方法**: Claude Code デスクトップアプリの設定 → MCP Servers → "Notion" で検索して追加

### Context7 MCP
- **できること**: npm/pip等のライブラリドキュメントを自動参照
- **品質管理との関連**: 既存解決策の活用（Development Philosophy）
- **追加方法**: Claude Code デスクトップアプリの設定 → MCP Servers → "Context7" で検索して追加

### Claude Preview
- **できること**: Webページの見た目をスクリーンショットで確認
- **品質管理との関連**: UI検証の3層検証Layer2（ISO9001 §8.6）
- **追加方法**: 追加不要（標準搭載）

## 任意

### Windows MCP
- **できること**: Windows操作の自動化（ウィンドウ管理・プロセス制御・レジストリ操作）
- **品質管理との関連**: 開発環境の自動構築・検証（ISO9001 §7.1）
- **追加方法**: Claude Code デスクトップアプリの設定 → MCP Servers → "Windows" で検索して追加

### Desktop Commander MCP
- **できること**: ファイル操作・コマンド実行・プロセス管理
- **品質管理との関連**: 運用自動化・バッチ処理（ISO9001 §8.5）
- **追加方法**: Claude Code デスクトップアプリの設定 → MCP Servers → "Desktop Commander" で検索して追加

### PDF MCP
- **できること**: PDF読み取り・作成・結合・分割・フォーム入力
- **品質管理との関連**: 設計書・仕様書の自動処理（ISO9001 §7.5）
- **追加方法**: Claude Code デスクトップアプリの設定 → MCP Servers → "PDF" で検索して追加

### GitHub MCP
- **できること**: Issue・PR操作、コード検索、Actions連携、リポジトリ管理
- **品質管理との関連**: GitHub Flow・変更管理・CI/CD（ISO9001 §8.1）
- **追加方法**: Claude Code デスクトップアプリの設定 → MCP Servers → "GitHub" で検索して追加（GitHub Token入力あり）

### Figma MCP
- **できること**: Figmaのデザインファイルを参照・コンポーネント情報取得
- **品質管理との関連**: 設計・開発管理（ISO9001 §8.3）
- **追加方法**: Claude Code デスクトップアプリの設定 → MCP Servers → "Figma" で検索して追加（APIキー入力あり）

## トラブルシューティング

MCP追加後にエラーが出た場合の対処法です。

| エラーパターン | 原因 | 対処 |
|--------------|------|------|
| `npx: command not found` | Node.js未インストール | https://nodejs.org/ からLTSインストール |
| `uvx: command not found` | uv未インストール | https://docs.astral.sh/uv/ からインストール |
| `EACCES: permission denied` | グローバルnpmの権限不足 | `npm config set prefix ~/.npm-global` + PATH追加 |
| `Error: Cannot find module` | npxキャッシュ破損 | `npx --yes clear-npx-cache` → 再試行 |
| `ETIMEOUT` / `ECONNREFUSED` | ネットワーク/プロキシ | `npm config set proxy` でプロキシ設定 |
| `401 Unauthorized` | APIキー未設定/期限切れ | 該当サービスでキーを再発行 |
| `spawn UNKNOWN` (Windows) | パスにスペース含む | パスをダブルクォートで囲む |
| MCP起動後すぐ切断 | ポート競合 or メモリ不足 | タスクマネージャーで競合確認、不要プロセスをkill |

### Windows固有の注意

- `npx` のパスに日本語やスペースが含まれるとエラーになることがある → `npm config get prefix` で確認
- `spawn UNKNOWN` エラーは Node.js の再インストールで解決することが多い
