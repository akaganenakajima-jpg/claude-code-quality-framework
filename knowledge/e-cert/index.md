# JDLA E資格（Deep Learning Engineer）知識ベース — インデックス

> 満点レベルのリファレンス。各ファイルは試験範囲を網羅し、数式・実装・実務活用を含む。

## ファイル一覧

| # | ファイル | 内容 | 主要トピック |
|---|---------|------|-------------|
| 1 | `dl-fundamentals.md` | 深層学習の基礎 | NN数理、誤差逆伝播、初期化、正則化、評価指標 |
| 2 | `dl-architectures.md` | 深層学習アーキテクチャ | CNN、RNN、Transformer、生成モデル、GNN |
| 3 | `dl-training.md` | 学習手法・最適化 | 最適化、分散学習、転移学習、蒸留、量子化 |
| 4 | `dl-applications.md` | 応用技術 | 物体検出、セグメンテーション、NLP、音声、強化学習 |

## 横断マップ — キーワード→参照先

| キーワード・業務 | 参照ファイル | セクション |
|-----------------|-------------|-----------|
| 活性化関数・損失関数・勾配 | `dl-fundamentals.md` | §1, §2 |
| 誤差逆伝播・自動微分・計算グラフ | `dl-fundamentals.md` | §2 |
| 重み初期化・Xavier・He | `dl-fundamentals.md` | §3 |
| 正則化・ドロップアウト・バッチ正規化 | `dl-fundamentals.md` | §4 |
| 評価指標・AUC・F1・BLEU | `dl-fundamentals.md` | §5 |
| CNN・畳み込み・ResNet・EfficientNet | `dl-architectures.md` | §1 |
| RNN・LSTM・GRU・Seq2Seq | `dl-architectures.md` | §2 |
| Transformer・Attention・BERT・GPT | `dl-architectures.md` | §3 |
| VAE・GAN・拡散モデル・フロー | `dl-architectures.md` | §4 |
| GNN・グラフ畳み込み | `dl-architectures.md` | §5 |
| SGD・Adam・学習率スケジューラ | `dl-training.md` | §1 |
| 分散学習・DeepSpeed・混合精度 | `dl-training.md` | §2 |
| 転移学習・LoRA・ファインチューニング | `dl-training.md` | §3 |
| 知識蒸留・Teacher-Student | `dl-training.md` | §4 |
| 量子化・プルーニング・エッジ推論 | `dl-training.md` | §5 |
| 物体検出・YOLO・Faster R-CNN | `dl-applications.md` | §1 |
| セグメンテーション・U-Net・DeepLab | `dl-applications.md` | §2 |
| NLP・トークナイザ・LLM | `dl-applications.md` | §3 |
| 音声認識・CTC・Whisper | `dl-applications.md` | §4 |
| 強化学習・DQN・PPO | `dl-applications.md` | §5 |
| マルチモーダル・CLIP・VQA | `dl-applications.md` | §6 |

## 試験対策の指針

### 頻出パターン
1. **計算問題**: 畳み込み出力サイズ、パラメータ数、受容野 → `dl-architectures.md` §1
2. **数式導出**: 逆伝播の連鎖律、損失関数の微分 → `dl-fundamentals.md` §1-§2
3. **比較問題**: Adam vs SGD、LSTM vs GRU、Pre-LN vs Post-LN → 各ファイルの比較表
4. **最新技術**: Transformer派生、拡散モデル、LoRA → `dl-architectures.md` §3-§4、`dl-training.md` §3

### 学習の優先順位
1. 基礎数理（`dl-fundamentals.md`）— 全問題の土台
2. Transformer（`dl-architectures.md` §3）— 出題頻度最高
3. 最適化（`dl-training.md` §1）— 計算問題頻出
4. 応用（`dl-applications.md`）— 概念理解中心
