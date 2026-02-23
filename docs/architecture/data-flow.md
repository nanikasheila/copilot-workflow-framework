# データフロー

最終更新: 2026-02-23

## 概要

本ドキュメントは、計算・履歴記録・エクスポートの主要データフローと Source of Truth を定義する。

## 計算フロー

```
呼び出し元
    │
    │  calculator.add(a, b) 等
    ▼
Calculator（src/calculator.py）
    │
    │  戻り値: float / int
    ▼
呼び出し元へ結果返却
```

- `Calculator` はステートレスに演算を実行し、結果を即時返却する
- 引数が不正な場合（例: ゼロ除算）は `ValueError` を送出する

## 履歴記録フロー

```
呼び出し元
    │
    │  Calculator(history=calculation_history).add(a, b) 等
    ▼
Calculator（src/calculator.py）
    │
    │  演算成功時のみ
    ▼
CalculationHistory.record(entry)（src/history.py）
    │
    │  CalculationEntry を追加
    ▼
CalculationHistory._entries: list[CalculationEntry]
```

- 演算が**成功した場合のみ** `CalculationHistory.record()` が呼ばれる
- `ValueError` 送出時（例外時）は `record()` は呼ばれず、履歴には記録されない
- `history` が `None`（DI なし）の場合も記録なしで正常に動作する

## エクスポートフロー

```
呼び出し元
    │
    │  calculation_history.export_to_json(path)
    ▼
CalculationHistory（src/history.py）
    │
    │  _entries をシリアライズ
    ▼
JSON ファイル（path で指定されたパス）
```

- `_entries` の全エントリを JSON 形式で出力する
- 出力先はパラメータ `path` で指定する

## 例外時のフロー

```
呼び出し元
    │
    │  calculator.divide(a, 0) 等
    ▼
Calculator（src/calculator.py）
    │
    │  ValueError を送出
    ▼
呼び出し元へ例外伝播
    ※ CalculationHistory.record() は呼ばれない
    ※ 履歴は変化しない
```

## Source of Truth

| データ | Source of Truth | 場所 |
|---|---|---|
| 計算履歴 | `CalculationHistory._entries` | `src/history.py` |
| 演算ロジック・バリデーション | `Calculator` メソッド | `src/calculator.py` |

- `CalculationHistory._entries` が履歴の**唯一の真実**である
- 他のオブジェクトやキャッシュは持たず、常に `_entries` を参照・更新する

## 変換ポイント

| ポイント | 変換内容 |
|---|---|
| `Calculator` → `CalculationHistory` | 演算結果を `CalculationEntry` データレコードに変換して記録 |
| `CalculationHistory` → JSON ファイル | `CalculationEntry` リストを JSON シリアライズ |
