# copilot-project-template

Reusable `.github` configuration template for Copilot-powered development workflows.

## 概要

プロジェクト横断で使える `.github` ディレクトリのテンプレートです。
GitHub Copilot のカスタムエージェント・スキル・ルール・インストラクションを体系的に管理します。

また、**Python** によるユーティリティモジュール（`src/math_utils.py`）を同梱しており、数値演算の共通処理をすぐに利用できます。

## 構造

`.github/` は **Instructions・Rules・Skills・Agents** の4層で構成されています。

```
.github/
├── copilot-instructions.md    # トップレベル Copilot 設定
├── settings.json              # プロジェクト固有設定
├── settings.schema.json       # settings.json のスキーマ
├── agents/                    # カスタムエージェント
│   ├── architect.agent.md     #   構造設計・設計判断
│   ├── developer.agent.md     #   実装・デバッグ・テスト
│   ├── manager.agent.md       #   影響分析・タスク分解・計画策定
│   ├── reviewer.agent.md      #   コードレビュー・品質・セキュリティ検証
│   └── writer.agent.md        #   ドキュメント・リリース管理
├── instructions/              # ファイルパターン別ガイドライン（applyTo で自動適用）
│   ├── common.instructions.md
│   ├── javascript.instructions.md
│   ├── typescript.instructions.md
│   ├── python.instructions.md
│   └── test.instructions.md
├── rules/                     # 開発ルール（常時適用）
│   ├── development-workflow.md
│   ├── branch-naming.md
│   ├── commit-message.md
│   ├── merge-policy.md
│   ├── worktree-layout.md
│   ├── issue-tracker-workflow.md
│   └── error-handling.md
└── skills/                    # ワークフロー手順（タスクに応じて自動ロード）
    ├── initialize-project/
    ├── start-feature/
    ├── submit-pull-request/
    ├── cleanup-worktree/
    ├── resolve-conflict/
    ├── merge-nested-branch/
    ├── generate-gitignore/
    └── skill-creator/
```

## エージェント

| エージェント | 役割 | 備考 |
|---|---|---|
| `architect` | 構造設計・設計判断 | ペースレイヤリング・非機能要求・データフロー観点で構造を評価 |
| `developer` | 実装・デバッグ・テスト | 実装モードとテストモードを切り替えて作業 |
| `manager` | 影響分析・タスク分解・計画策定 | 全変更で影響分析を実施し、必要時 architect にエスカレーション |
| `reviewer` | コードレビュー・品質・セキュリティ検証 | 修正指示を構造化して出力。セキュリティ観点を常時チェック |
| `writer` | ドキュメント・リリース管理 | 技術文書・リリースノート・バージョニング |

### エージェント連携フロー

```
1. manager に影響分析・タスク分解を依頼
2. エスカレーション該当時、architect に構造評価・配置判断を依頼
3. manager に計画策定を依頼 → 実行計画を受領
4. developer に実装を依頼
5. reviewer にレビューを依頼
6. LGTM まで 5-6 を繰り返す
7. writer にドキュメント更新を依頼（必要な場合）
```

## 使い方

1. このリポジトリの `.github/` を自分のプロジェクトにコピー
2. `settings.json` をプロジェクトに合わせて編集（または `initialize-project` スキルで初期化）
3. Copilot Chat でエージェントを活用

## ツール利用ポリシー

| ツール | 必須度 | 備考 |
|---|---|---|
| Git | **必須** | すべての変更は Git で管理 |
| GitHub | **推奨** | PR・マージ・コードレビューに使用 |
| Issue トラッカー | **オプション** | Linear / GitHub Issues / Jira 等、`provider: "none"` で無効化可能 |

## Python ユーティリティ

### math_utils モジュール

`src/math_utils.py` は、よく使う数値演算を純粋関数として提供するモジュールです。

#### 利用可能な関数

| 関数 | シグネチャ | 説明 |
|---|---|---|
| `add` | `add(a: float, b: float) -> float` | 加算 |
| `subtract` | `subtract(a: float, b: float) -> float` | 減算 |
| `multiply` | `multiply(a: float, b: float) -> float` | 乗算 |
| `divide` | `divide(a: float, b: float) -> float` | 除算（ゼロ除算時は `ZeroDivisionError`） |
| `power` | `power(base: float, exp: float) -> float` | べき乗 |
| `factorial` | `factorial(n: int) -> int` | 階乗（非負整数のみ、負数は `ValueError`） |
| `fibonacci` | `fibonacci(n: int) -> list[int]` | フィボナッチ数列の先頭 n 項（非負整数のみ） |

#### 使い方

```python
from src.math_utils import add, divide, factorial, fibonacci

# 基本演算
result = add(3, 5)        # 8
result = divide(10, 4)    # 2.5

# ゼロ除算はエラー
try:
    divide(1, 0)
except ZeroDivisionError as e:
    print(e)  # "divisor 'b' must not be zero"

# 階乗
result = factorial(5)     # 120

# フィボナッチ数列
result = fibonacci(10)    # [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]
```

### テスト実行

```bash
python -m pytest tests/ -v --tb=short
```

- テストファイル: `tests/test_math_utils.py`
- テスト数: 40件
- カバレッジ: 100%

## ライセンス

MIT
