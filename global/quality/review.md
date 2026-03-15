# 検証基準 — 3層検証 (ISO9001 §8.6/§9.1)

成果物は以下3層の検証を順に通過すること。層の飛ばし禁止。

## Layer 1: ユニットテスト
- `vitest` 全件PASS（既存テスト含む）
- 新機能にはテスト追加必須（TDD — G2準拠）
- 失敗時 → 修正してLayer 1を再実行

## Layer 2: E2Eテスト
- `bash e2e_test.sh` 全件PASS
- UI変更時は6Phaseデバッグループも実施
- 失敗時 → 修正してLayer 1から再実行

## Layer 3: 本番検証（デプロイ時のみ）
- `deploy-protocol.md` 全チェック実施
  - API疎通（/api/health）
  - 残高異常値チェック
  - 外部監視UP確認
- 失敗時 → ロールバック → 修正 → Layer 1から再実行

## 6Phaseループとの関係
Layer 2の拡張手順として、UI/機能変更時に `test-debug-loop-protocol.md` を適用する。
