# dsh-hs-candidate

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

## Development

```sh
pnpm install --frozen-lockfile
pnpm build && pnpm lint && pnpm typecheck && pnpm test && pnpm gate:sku13
```

## License

Apache-2.0. See `LICENSE`, `NOTICE`, `THIRD-PARTY-NOTICES`.
