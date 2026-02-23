# 用語集

最終更新: 2026-02-23

本プロジェクト固有のドメイン用語と設計用語を定義する。
LLM および開発者がコードを読む際の共通認識として使用する。

---

## ドメイン用語

### Calculator

**四則演算を提供するドメイン計算層のクラス。**

- `src/calculator.py` に定義される
- 加算・減算・乗算・除算をステートレスなメソッドとして提供する
- バリデーション（ゼロ除算禁止等）を内包し、不正入力は `ValueError` で通知する
- オプショナル DI により `CalculationHistory` を受け取ることができる
- 参照: [module-map.md](module-map.md)

### CalculationHistory

**計算結果の記録・エクスポートを担うアプリケーション記録層のクラス。**

- `src/history.py` に定義される
- `CalculationEntry` を時系列で保持し、JSON ファイルへのエクスポート機能を提供する
- `_entries` リストが履歴の Source of Truth である
- `Calculator` からオプショナル DI で注入される（`Calculator` への逆依存は禁止）
- 参照: [module-map.md](module-map.md), [data-flow.md](data-flow.md)

### CalculationEntry

**1回の計算操作とその結果を表すイミュータブルなデータレコード。**

- `src/history.py` に定義される
- 操作種別（`add` / `subtract` / `multiply` / `divide`）、オペランド、結果、タイムスタンプを保持する
- `CalculationHistory.record()` 経由でのみ生成・追加される
- イミュータブルとして扱い、生成後の変更は行わない

---

## 設計用語

### ペースレイヤリング

**変化速度の異なる層を分離し、遅い層が速い層に依存しない設計原則。**

- 変化速度が低い層（安定層）は、変化速度が高い層（不安定層）に依存してはならない
- 本プロジェクトでは `calculator.py`（安定層）が `history.py`（不安定層）を直接インスタンス化することを禁止する
- 参照: [ADR-001.md](adr/ADR-001.md)

### DI（依存性注入）

**依存オブジェクトを外部から注入する設計パターン。**

- Dependency Injection の略
- オブジェクト内部で依存オブジェクトを生成するのではなく、コンストラクタや引数経由で外部から渡す
- 本プロジェクトでは `Calculator` が `CalculationHistory` をコンストラクタ引数で受け取る形を採用する
- テスト時にモックを注入できるため、テスタビリティが向上する
- 参照: [ADR-001.md](adr/ADR-001.md)

### Source of Truth

**ある情報の唯一の信頼できる出所。**

- 同一データを複数箇所で保持しないことで、整合性の問題を防ぐ
- 本プロジェクトでは `CalculationHistory._entries` が計算履歴の Source of Truth である
- 参照: [data-flow.md](data-flow.md)
