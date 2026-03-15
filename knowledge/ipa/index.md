# システム開発 知識ベース — インデックス

## ファイル一覧

| # | ファイル | 分野 | 主な内容 |
|---|---|---|---|
| 1 | `fe.md` | 基礎理論・CS | アルゴリズム・データ構造・離散数学・CPU/メモリ・OS |
| 2 | `ap.md` | 応用技術 | 待ち行列理論・パイプライン・SQL応用・VPN・EVM |
| 3 | `db.md` | データベース | 正規化(1NF-5NF)・SQL高度技法・MVCC・分散DB |
| 4 | `nw.md` | ネットワーク | OSPF/BGP・VPN/IPsec・SD-WAN・DNS・TLS |
| 5 | `es.md` | 組込み・IoT | RTOS・安全設計(IEC61508)・通信(CAN/BLE/LoRa) |
| 6 | `pm.md` | プロジェクト管理 | PMBOK・EVM・CPM/PERT・FP法・アジャイル |
| 7 | `sm.md` | サービス運用 | ITIL4・SLA/MTBF/MTTR・BCP/DR・CMDB |
| 8 | `st.md` | IT戦略・経営 | SWOT/5Forces・NPV/IRR・DX戦略・BSC |
| 9 | `sa.md` | アーキテクチャ | マイクロサービス・CQRS・DDD・性能設計・移行戦略 |
| 10 | `au.md` | 監査・内部統制 | COSO・J-SOX・CAAT・COBIT・3線モデル |

## 分野横断マップ — どの業務でどのファイルを参照するか

| 業務シーン | 主参照 | 補助参照 |
|---|---|---|
| コードレビュー・アルゴリズム最適化 | `fe.md` | `ap.md` |
| DB設計・SQL最適化・トランザクション設計 | `db.md` | `fe.md`, `sa.md` |
| インフラ・NW設計・障害対応 | `nw.md` | `sm.md` |
| セキュリティ設計・脅威分析 | `nw.md` | `au.md`, `sa.md` |
| プロジェクト管理・見積り・進捗評価 | `pm.md` | `st.md` |
| 運用設計・SLA策定・障害管理 | `sm.md` | `nw.md`, `au.md` |
| IT投資判断・DX戦略・ビジネス分析 | `st.md` | `pm.md` |
| アーキテクチャ設計・技術選定 | `sa.md` | `db.md`, `nw.md` |
| 組込み・IoTシステム設計 | `es.md` | `nw.md`, `sa.md` |
| 内部統制・コンプライアンス・監査対応 | `au.md` | `sm.md`, `st.md` |

## 横断テーマ別索引

| テーマ | 関連ファイル |
|---|---|
| セキュリティ | `nw.md`(NWセキュリティ), `sa.md`(セキュリティアーキテクチャ), `au.md`(セキュリティ監査), `es.md`(セキュアブート) |
| 可用性・信頼性 | `sa.md`(信頼性設計), `sm.md`(可用性管理/MTBF/MTTR), `nw.md`(冗長化/VRRP) |
| 性能・スケーラビリティ | `sa.md`(性能設計), `db.md`(インデックス/パーティション), `nw.md`(帯域設計), `ap.md`(待ち行列理論) |
| コスト・投資判断 | `st.md`(NPV/IRR/ROI), `pm.md`(EVM/見積り), `sm.md`(TCO/課金) |
| 品質管理 | `pm.md`(QC7つ道具), `sa.md`(テスト戦略), `sm.md`(継続的改善) |
| クラウド | `sa.md`(クラウドアーキテクチャ), `nw.md`(SD-WAN/SASE), `au.md`(クラウド監査) |
