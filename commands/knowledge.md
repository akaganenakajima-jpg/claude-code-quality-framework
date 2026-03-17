# /knowledge — 知識ベース参照

課題を分析し、必要な知識ファイルを特定して参照する。

## 手順

1. ユーザーの課題/質問を分析する
2. CLAUDE.md §知識ベース自動参照 の2層構造で分類する:
   - **Step 1（大分類）**: 12カテゴリから該当を全て特定
   - **Step 2（横断チェック）**: 6観点を全て走査
3. 該当する知識ファイルを `~/.claude/knowledge/` から Read する
4. 参照した内容を要約し、課題への適用方法を提示する

## 知識ファイルの場所

- IPA系: `~/.claude/knowledge/ipa/`
- 統計: `~/.claude/knowledge/stats/`
- DS発展: `~/.claude/knowledge/ds-advanced/`
- DSエキスパート: `~/.claude/knowledge/ds-expert/`
- 数学: `~/.claude/knowledge/math-strategist/`
- E資格: `~/.claude/knowledge/e-cert/`
- Python: `~/.claude/knowledge/python3/`
- 開発プラクティス: `~/.claude/knowledge/practices/`

$ARGUMENTS に課題の説明がある場合はそれを分析対象にする。
ない場合は現在のコンテキストから課題を推定する。
