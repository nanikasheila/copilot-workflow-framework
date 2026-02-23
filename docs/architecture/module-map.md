# モジュールマップ

最終更新: 2026-02-23

## ディレクトリ構造と責務

```
src/
├── __init__.py
├── calculator.py        # ドメイン計算層
└── history.py           # アプリケーション記録層
tests/
├── __init__.py
└── test_calculator.py   # 単体テスト
```

## 層の対応

| モジュール | 層 | 責務 | 変化速度 | 安定度 |
|---|---|---|---|---|
| `src/calculator.py` | ドメイン計算層 | 四則演算ロジックの提供 | 低 | 高 |
| `src/history.py` | アプリケーション記録層 | 計算結果の記録・エクスポート | 中〜高 | 中 |

### ドメイン計算層 — `src/calculator.py`

- `Calculator` クラスを定義する
- 四則演算（加減乗除）をステートレスに提供する
- ビジネスルール（ゼロ除算禁止等）を内包する
- 変化速度が低く、他のモジュールが依存してよい安定した層

### アプリケーション記録層 — `src/history.py`

- `CalculationEntry` データレコードと `CalculationHistory` クラスを定義する
- 計算結果を時系列で記録し、JSON エクスポートを提供する
- 機能要求に応じて変化しやすいため、ドメイン計算層より上位の層に置く
- ドメイン計算層（`calculator.py`）への依存は禁止する

## 依存方向

```
呼び出し元
    │
    ▼
calculator.py  ──(オプショナル DI)──▶  history.py
    │                                      │
    │  ◀──────── 依存禁止 ───────────────┘
    │
    ▼
結果返却
```

### ルール

- `calculator.py` は `history.py` をオプショナル DI（`Optional[CalculationHistory] = None`）で受け取ることができる
- 型チェック時のみインポートする（`TYPE_CHECKING` ガード）
- `history.py` から `calculator.py` への依存は**禁止**（ペースレイヤリング違反）
- DI を使わない場合、`Calculator` は単独で動作する（後方互換）

### 設計判断

DI 方式の詳細は [adr/ADR-001.md](adr/ADR-001.md) を参照。
