# 故障排查 — dsh-hs-candidate

每条按「症状 / 原因 / 动作」写。报错原文都是 `<一句人话>（E_XXX）｜下一步：<动作>`，
把 `E_XXX` 和这句话一起发到 issue 即可定位；不要把真实报关单贴进 issue。

## 1. 产品描述为空（E_HS_DESCRIPTION_MISSING）

- **症状**：`产品描述是空的，没法给出候选编码（E_HS_DESCRIPTION_MISSING）｜下一步：用一句话写清材质、用途和功能再试`
- **原因**：`description` 传了空字符串，或只传了空格。
- **动作**：至少写成「材质 + 用途 + 功能」，例如 `plastic housing for electric motor`，再调 `hs.classify`。

## 2. HS 编码位数或字符不对（E_HS_CODE_LENGTH / E_HS_CODE_FORMAT）

- **症状**：`HS 编码位数不对（E_HS_CODE_LENGTH）｜下一步：用 2/4/6/8/10 位，例如 8471.30 或 84713000`
- **原因**：把 5 位、7 位、9 位编码当成有效编码，或把章节标题 / 字母混进了编码。
- **动作**：只保留数字和点，长度改为 2/4/6/8/10 位；国内 8/10 位编码请确认最后两位是本国的附加码。

## 3. 编码落在保留章（E_HS_CODE_CHAPTER_RESERVED）

- **症状**：`这个章节号（00 或 98/99）是保留章，不能直接归类（E_HS_CODE_CHAPTER_RESERVED）｜下一步：换成 01–97 章的真实编码，或交人工复核`
- **原因**：用了 `0000` / `9999.00` 这类占位编码，或把 98/99 章当成普通商品章。
- **动作**：换成 01–97 章的真实编码，再用 `hs.code_check` 复验；仍不确定就交人工归类，工具不做海关裁定。

## 还不行

```sh
node samples/quickstart/run.mjs --check   # 自带样例必须通过
node --test test/*.test.mjs               # 13 项测试
```

仍失败时请在 <https://github.com/PerryLink/dsh-hs-candidate/issues> 附上：包版本、最小合成输入、完整报错那一行。
