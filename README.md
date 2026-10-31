# dsh-hs-candidate

> 🧊 **FROZEN — 2026-10-31. No new features.** This public/synthetic S1 demo is not GA; it stays installable and only genuine breakage is fixed.

## Maintenance status: 🧊 FROZEN

Frozen on 2026-10-31. This repository is a public/synthetic S1 demo, not a validated product. The npm package stays installable; no new features are planned.


HS Top-3 candidates, 12-element completeness, RVC check and tariff version gate for DeepSeek Harness.

> **Status: alpha / public-synthetic / partial / not counted / not GA.** No customer evidence, customer data, or production-readiness claim. All acceptance rows are `counted=false`.

## Install

```sh
dsh plugin --profile <profile> add dsh-hs-candidate
dsh --profile <profile> --dump-config | grep dsh-hs-candidate
```

Requires DSH `>=0.2.1-rc.3 <0.3.0` and Node `>=24.9 <25`.

<details>
<summary>中文摘要</summary>

HS Top3 候选、12 要素完整性、RVC 与税则版本门。 安装：`dsh plugin --profile <profile> add dsh-hs-candidate`。公开/合成、alpha、非 GA。

</details>

## Tools

| Tool | What it does | Risk |
|---|---|---|
| `hs.elements` | Check the 12-element completeness of a product description | R0 |
| `hs.classify` | Return Top-3 HS candidates from a public table | R0 |
| `hs.lookup` | Look up a public HS table row | R0 |
| `hs.tariff_version` | Record/check the tariff table version | R0 |
| `hs.rvc_check` | Compute a simple regional value content ratio | R0 |

## Input / output

**Input:** a product description and a tariff table version. **Output:** Top-3 candidate codes, missing 12-element fields, and a simple RVC ratio. Candidates are evidence for human review, not a legal classification.

## Limits / non-claims

- Not a legal classification, customs ruling, origin determination, or filing.
- No four-list screening, broker integration, or Client surface.
- Public HS lookup sample only; no customer declaration or broker data.
- No customer evidence, customer data, or production-readiness claim; all fixtures are public/synthetic.

## Public sample

MIT HS lookup sample; `ACCEPTANCE.csv` lists 5 public checks.

## 中文说明

HS Top3 候选、12 要素完整性、RVC 检查与税则版本门。**公开/合成、alpha、非 GA**；候选码不是法律归类。

### 安装

```sh
dsh plugin --profile <profile> add dsh-hs-candidate
```

### 工具

| 工具 | 作用 |
|---|---|
| `hs.elements` | 检查商品描述的 12 要素完整性 |
| `hs.classify` | 从公开税则表返回 Top3 候选 |
| `hs.lookup` | 查询公开 HS 表行 |
| `hs.tariff_version` | 记录/校验税则表版本 |
| `hs.rvc_check` | 简单区域价值成分比例 |

### 输入 / 输出

输入商品描述与税则版本；输出候选码、缺失要素和简单 RVC 比例。候选只作人工复核证据。

### 边界

- 不是法律归类、海关裁定、原产地判定或申报。
- 不做四张清单筛查、不接报关行、无 Client。
- 只有公开 HS 样例，没有客户报关数据。

## Development

```sh
pnpm install --frozen-lockfile
pnpm build && pnpm lint && pnpm typecheck && pnpm test && pnpm gate:sku13
```

## License

Apache-2.0. See `LICENSE`, `NOTICE`, `THIRD-PARTY-NOTICES`.
