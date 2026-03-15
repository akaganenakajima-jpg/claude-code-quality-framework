# 推奨ツール・MCP一覧

Claude Codeの品質管理フレームワークと連携して効果を発揮するツール群です。
全て任意ですが、「おすすめ」マークのツールは導入を推奨します。

## おすすめ

### Notion MCP
- **できること**: Notionにドキュメントを自動記録・検索・更新
- **品質管理との関連**: 文書管理・記録保持（ISO9001 §7.5）
- **追加方法**: Claude Code GUI の設定 → MCP Servers → Notion を追加

### Context7 MCP
- **できること**: npm/pip等のライブラリドキュメントを自動参照
- **品質管理との関連**: 既存解決策の活用（Development Philosophy）
- **追加方法**: Claude Code GUI の設定 → MCP Servers → Context7 を追加

### Claude Preview
- **できること**: Webページの見た目をスクリーンショットで確認
- **品質管理との関連**: UI検証の3層検証Layer2（ISO9001 §8.6）
- **追加方法**: Claude Code に標準搭載（追加設定不要）

## 任意

### Figma MCP
- **できること**: Figmaのデザインファイルを参照・コンポーネント情報取得
- **品質管理との関連**: 設計・開発管理（ISO9001 §8.3）
- **追加方法**: Claude Code GUI の設定 → MCP Servers → Figma を追加
- **前提**: Figma APIキーが必要

### Google Drive MCP
- **できること**: Google Driveのファイルを検索・読み取り
- **品質管理との関連**: 文書共有（ISO9001 §7.4）
- **追加方法**: Claude Code GUI の設定 → MCP Servers → Google Drive を追加

### Box MCP
- **できること**: Boxのファイルを検索・読み取り・アップロード
- **品質管理との関連**: 文書共有（ISO9001 §7.4）
- **追加方法**: Claude Code GUI の設定 → MCP Servers → Box を追加
