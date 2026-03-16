# 推奨ツール・MCP一覧

Claude Codeの品質管理フレームワークと連携して効果を発揮するツール群です。
全て任意ですが、「おすすめ」マークのツールは導入を推奨します。

## 前提条件

MCPサーバーは `npx` または `uvx` で起動するものが大半です。導入前に確認してください。

| 前提 | 確認コマンド | 未インストール時 |
|------|------------|----------------|
| Node.js (≥18) | `node --version` | https://nodejs.org/ からLTSをインストール |
| npx | `npx --version` | Node.jsに同梱。`npm install -g npm` で更新 |
| Python (≥3.10) | `python3 --version` | https://www.python.org/ からインストール |
| uvx | `uvx --version` | `pip install uv` または `curl -LsSf https://astral.sh/uv/install.sh \| sh` |

## おすすめ

### Notion MCP
- **できること**: Notionにドキュメントを自動記録・検索・更新
- **品質管理との関連**: 文書管理・記録保持（ISO9001 §7.5）
- **前提**: npx（Node.js）
- **追加方法**: Claude Code GUI の設定 → MCP Servers → Notion を追加

### Context7 MCP
- **できること**: npm/pip等のライブラリドキュメントを自動参照
- **品質管理との関連**: 既存解決策の活用（Development Philosophy）
- **前提**: npx（Node.js）
- **追加方法**: Claude Code GUI の設定 → MCP Servers → Context7 を追加

### Claude Preview
- **できること**: Webページの見た目をスクリーンショットで確認
- **品質管理との関連**: UI検証の3層検証Layer2（ISO9001 §8.6）
- **前提**: なし（Claude Code標準搭載）
- **追加方法**: 追加不要

## 任意

### Figma MCP
- **できること**: Figmaのデザインファイルを参照・コンポーネント情報取得
- **品質管理との関連**: 設計・開発管理（ISO9001 §8.3）
- **前提**: npx + Figma APIキー
- **追加方法**: Claude Code GUI の設定 → MCP Servers → Figma を追加

### Google Drive MCP
- **できること**: Google Driveのファイルを検索・読み取り
- **品質管理との関連**: 文書共有（ISO9001 §7.4）
- **前提**: npx + Google OAuth認証
- **追加方法**: Claude Code GUI の設定 → MCP Servers → Google Drive を追加

### Box MCP
- **できること**: Boxのファイルを検索・読み取り・アップロード
- **品質管理との関連**: 文書共有（ISO9001 §7.4）
- **前提**: npx + Box認証
- **追加方法**: Claude Code GUI の設定 → MCP Servers → Box を追加

## トラブルシューティング

MCP追加後にエラーが出た場合の対処法です。

| エラーパターン | 原因 | 対処 |
|--------------|------|------|
| `npx: command not found` | Node.js未インストール | https://nodejs.org/ からLTSインストール |
| `uvx: command not found` | uv未インストール | `pip install uv` |
| `EACCES: permission denied` | グローバルnpmの権限不足 | `npm config set prefix ~/.npm-global` + PATH追加 |
| `Error: Cannot find module` | npxキャッシュ破損 | `npx --yes clear-npx-cache` → 再試行 |
| `ETIMEOUT` / `ECONNREFUSED` | ネットワーク/プロキシ | `npm config set proxy` でプロキシ設定 |
| `401 Unauthorized` | APIキー未設定/期限切れ | 該当サービスでキーを再発行 |
| `spawn UNKNOWN` (Windows) | パスにスペース含む | パスをダブルクォートで囲む |
| MCP起動後すぐ切断 | ポート競合 or メモリ不足 | `lsof -i :PORT` で競合確認、不要プロセスをkill |

### Windows固有の注意

- `npx` のパスに日本語やスペースが含まれるとエラーになることがある → `npm config get prefix` で確認
- PowerShellとGit Bashで `PATH` が異なる場合がある → Git Bashで `which npx` で確認
- `spawn UNKNOWN` エラーは Node.js の再インストールで解決することが多い
