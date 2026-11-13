#!/usr/bin/env python3
"""README visuals for dsh-hs-candidate — drawn from what this repo ships.

Two figures, both derived from the plugin's own source and its bundled
quickstart run (not from a generic pipeline template):

  hero 1440x576 (Pillow, four files: zh/en x light/dark)
      The artifact this plugin produces, one classification record:
      the description "plastic housing for electric motor" from
      samples/quickstart/input/descriptions.csv, the Top-3 shortlist that
      src/core/hs.ts CANDIDATES actually returns for it (3926.90, 8501.10,
      7326.90) with the confidence values the code assigns (0.9 / 0.75 /
      0.6) and the exact GIR wording ("GIR 1 + heading text" first,
      "GIR 1 fallback; verify with GIR 3/6" after), then the 12 required
      element keys from ELEMENTS drawn as an all-missing grid
      (missing_when_omitted = 12 in the golden file), and the record sink
      $DSH_HOME/storages/hs/ with the content id hs_f926f0d8616f — the
      first 12 hex chars of sha256("plastic housing for electric motor"),
      which is how src/plugin/tools.ts builds classification_id.

  flow 1100x660 (hand-written SVG, two files: light/dark)
      Grammar: a KEYWORD BRANCH TREE, not a row of boxes. The search text
      (description + supplied element values) enters a five-entry public
      keyword table; the five real entries branch out with representative
      keywords from their regexes, the two that this sample matches are
      marked and the other three end as misses. The matched codes feed the
      Top-3 shortlist on the right, where the third slot is filled by table
      order (which is exactly what candidates() does: hits first, then the
      remaining entries in table order). The record strip carries tariff
      2026.1 and the 12 missing elements (the sample calls classify with the
      description only; elements.json is optional, and the golden file
      records missing_when_omitted = 12). The R0 bench lists the read-only
      tools with values from the golden run / acceptance script (code_check
      84713000 valid / 9999.00 reserved chapter; rvc_report 30 / 60 / 60;
      rvc_check 50% >= 40 from scripts/acceptance.mjs; lookup at most 5
      rows from source).

Facts used here, verified against the repository:
  src/core/hs.ts        ELEMENTS(12), CANDIDATES(5 + 9999.00 fallback),
                        confidence 0.9 - 0.15*i, GIR wording, TARIFF_VERSION
                        '2026.1', code_check 2/4/6/8/10 + chapters 01-97,
                        rvc_report three methods
  src/plugin/tools.ts   classification_id = 'hs_' + sha256(description)[:12];
                        classify writes missing_elements; rvc_check default
                        threshold 40; lookup slice(0, 5)
  src/plugin/storage.ts classifications table fields (classification_id,
                        description, tariff_version, top3, missing_elements,
                        created_at)
  samples/quickstart/expected/result.json
                        the golden run quoted above (top3 order, 12 missing
                        when omitted, tariff 2026.1, code checks, RVC 30/60/60)

Run:  python scripts/gen-readme-assets.py
Needs: Pillow, and the Windows fonts msyh.ttc / msyhbd.ttc / consola.ttf /
       consolab.ttf. A missing font aborts instead of shipping tofu boxes.
"""
from __future__ import annotations

import math
import os
from html import escape

from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "docs", "assets")

FONT_CJK = r"C:\Windows\Fonts\msyh.ttc"
FONT_CJK_BOLD = r"C:\Windows\Fonts\msyhbd.ttc"
FONT_MONO = r"C:\Windows\Fonts\consola.ttf"
FONT_MONO_BOLD = r"C:\Windows\Fonts\consolab.ttf"
for _p in (FONT_CJK, FONT_CJK_BOLD, FONT_MONO, FONT_MONO_BOLD):
    if not os.path.exists(_p):
        raise SystemExit(f"FATAL: font missing: {_p}")

RADIUS = 22
SHADOW = 26

SKIN = {
    "light": dict(
        bg_from="#f9f6fd", bg_to="#e4eaf8",
        card="#ffffff", card_edge="#e6e2ef",
        text="#141419", sub="#4d5261", faint="#8f94a4",
        accent="#4B67B4", accent2="#16a34a",
        pill="#ece7f9", band="#f5f2fb", grid="#e7e4f0",
        mark="#b45309", mark_bg="#fdf3e9",
        on_accent="#ffffff",
        shadow=(32, 26, 64), glow2="#7a68c9",
    ),
    "dark": dict(
        bg_from="#131a2a", bg_to="#0c1016",
        card="#1b2231", card_edge="#2e374b",
        text="#f0f3f9", sub="#a8b1c4", faint="#737b8d",
        accent="#8496f5", accent2="#3fb950",
        pill="#242d42", band="#202839", grid="#262f42",
        mark="#d9a441", mark_bg="#2a2216",
        on_accent="#0c1016",
        shadow=(0, 0, 0), glow2="#8496f5",
    ),
}

FONT_FILES = {"cjk": FONT_CJK, "cjk_bold": FONT_CJK_BOLD,
              "mono": FONT_MONO, "mono_bold": FONT_MONO_BOLD}


def font(size: float, kind: str = "cjk_bold") -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(FONT_FILES[kind], size)


def hx(s: str) -> tuple[int, int, int]:
    s = s.lstrip("#")
    return tuple(int(s[i:i + 2], 16) for i in (0, 2, 4))


def gradient(w: int, h: int, c1: str, c2: str) -> Image.Image:
    base = Image.new("RGB", (w, h))
    d = ImageDraw.Draw(base)
    a, b = hx(c1), hx(c2)
    for y in range(h):
        t = 0.15 * (y / h) + 0.85 * (y / h) ** 1.35
        d.line([(0, y), (w, y)],
               fill=tuple(int(p + (q - p) * t) for p, q in zip(a, b)))
    return base


def glow(img: Image.Image, cx: int, cy: int, r: int, color: tuple,
         alpha: int = 40) -> Image.Image:
    layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    for i in range(9, 0, -1):
        rr = r * i / 9
        d.ellipse([cx - rr, cy - rr, cx + rr, cy + rr],
                  fill=color + (int(alpha * (1 - i / 10)),))
    return Image.alpha_composite(img.convert("RGBA"), layer).convert("RGB")


def card(img: Image.Image, box: tuple, s: dict, radius: int = RADIUS,
         shadow: int = SHADOW, fill: str | None = None) -> Image.Image:
    x0, y0, x1, y1 = box
    sh = Image.new("RGBA", img.size, (0, 0, 0, 0))
    sd = ImageDraw.Draw(sh)
    for i in range(shadow, 0, -3):
        sd.rounded_rectangle([x0 - i // 5, y0 + i // 2, x1 + i // 5, y1 + i],
                             radius=radius + i // 5,
                             fill=s["shadow"] + (int(9 * (1 - i / shadow)),))
    base = Image.alpha_composite(img.convert("RGBA"),
                                 sh.filter(ImageFilter.GaussianBlur(10)))
    d = ImageDraw.Draw(base)
    d.rounded_rectangle(box, radius=radius, fill=hx(fill or s["card"]),
                        outline=hx(s["card_edge"]), width=2)
    return base.convert("RGB")


_SCRATCH = ImageDraw.Draw(Image.new("RGB", (8, 8)))


def measure(text: str, size: float, kind: str) -> float:
    return _SCRATCH.textlength(text, font=font(size, kind))


def require_w(text: str, size: float, kind: str, max_w: float,
              what: str) -> None:
    w = measure(text, size, kind)
    if w > max_w + 0.4:
        raise SystemExit(f"FATAL: {what} overflows: {text!r} needs "
                         f"{w:.1f}px > {max_w}px")


def fit(text: str, kind: str, max_w: float, start: float,
        minimum: float) -> float:
    size = start
    while size > minimum:
        if measure(text, size, kind) <= max_w:
            return size
        size -= 1
    if measure(text, size, kind) <= max_w:
        return size
    raise SystemExit(f"FATAL: text does not fit {max_w}px at >= {minimum}px: "
                     f"{text!r}")


def fit_lines(lines: list[str], kind: str, max_w: float, start: float,
              minimum: float) -> float:
    return min(fit(t, kind, max_w, start, minimum) for t in lines)


def pill(img: Image.Image, xy: tuple[int, int], text: str, s: dict,
         size: float = 16, fg: str | None = None, bg: str | None = None,
         kind: str = "cjk_bold") -> tuple[int, int]:
    d = ImageDraw.Draw(img)
    f = font(size, kind)
    w = d.textlength(text, font=f)
    x, y = xy
    h = size + 20
    d.rounded_rectangle([x, y, x + w + 30, y + h], radius=h // 2,
                        fill=hx(bg or s["pill"]))
    d.text((x + 15, y + h / 2), text, font=f, fill=hx(fg or s["accent"]),
           anchor="lm")
    return int(x + w + 30), int(y + h)


def chip(img: Image.Image, xy: tuple[int, int], text: str, fg: str, bg: str,
         size: float = 11, kind: str = "cjk_bold", padx: int = 9,
         height: int = 20, anchor_right: bool = False) -> int:
    d = ImageDraw.Draw(img)
    f = font(size, kind)
    w = d.textlength(text, font=f)
    x, y = xy
    if anchor_right:
        x = x - w - padx * 2
    d.rounded_rectangle([x, y, x + w + padx * 2, y + height],
                        radius=height / 2, fill=hx(bg))
    d.text((x + padx, y + height / 2), text, font=f, fill=hx(fg),
           anchor="lm")
    return int(w + padx * 2)


def dash_rect(d: ImageDraw.ImageDraw, box: tuple[float, float, float, float],
              color: str, width: int = 2, dash: int = 7,
              gap: int = 5) -> None:
    x0, y0, x1, y1 = box
    for a, b in (((x0, y0), (x1, y0)), ((x0, y1), (x1, y1)),
                 ((x0, y0), (x0, y1)), ((x1, y0), (x1, y1))):
        dist = math.hypot(b[0] - a[0], b[1] - a[1])
        if dist == 0:
            continue
        n = int(dist // (dash + gap)) + 1
        for i in range(n):
            t0 = i * (dash + gap) / dist
            t1 = min((i * (dash + gap) + dash) / dist, 1.0)
            if t0 >= 1:
                break
            d.line([(a[0] + (b[0] - a[0]) * t0, a[1] + (b[1] - a[1]) * t0),
                    (a[0] + (b[0] - a[0]) * t1, a[1] + (b[1] - a[1]) * t1)],
                   fill=hx(color), width=width)


# --------------------------------------------------------------------------- hero
# The values below are the bundled quickstart's own record, not invented data:
# description row 1 of samples/quickstart/input/descriptions.csv, the Top-3
# order in expected/result.json, confidence and GIR wording from CANDIDATES/
# candidates(), and the id that sha256 of that description produces.
DESCRIPTION = "plastic housing for electric motor"
CLASSIFICATION_ID = "hs_f926f0d8616f"  # sha256(DESCRIPTION)[:12]
CANDIDATES = [
    ("3926.90", "Other articles of plastics", 0.90, "GIR 1 + heading text"),
    ("8501.10", "Motors of output <= 37.5 W", 0.75,
     "GIR 1 fallback; verify with GIR 3/6"),
    ("7326.90", "Other articles of iron or steel", 0.60,
     "GIR 1 fallback; verify with GIR 3/6"),
]
ELEMENTS = [
    "product_name", "material", "function", "use", "composition",
    "processing", "packaging", "brand", "model", "spec", "origin", "unit",
]

HERO = {
    "zh": dict(
        kicker="DeepSeek Harness 插件 · HS 归类候选",
        value=["一句产品描述，先给 3 个 HS 候选；",
               "12 项归类要素，缺哪项一次列清。"],
        sub="按公开关键词表给候选与 GIR 依据；本机算，不联网。",
        meta="7 个工具 · TARIFF_VERSION 2026.1 · R1 只写本地",
        foot="Apache-2.0 · PerryLink DSH plugin family",
        rec_title="归类记录 · hs_classify",
        rec_chip="R1 本地写",
        ver_chip="2026.1",
        desc_label="描述",
        conf_label="置信度",
        rec_foot="置信度是排序提示（0.9 / 0.75 / 0.6），不是概率 · "
                 "首位 GIR 1 + 品目条文",
        elements_title="12 要素完整性",
        elements_chip="missing 12",
        elements_foot="仅传描述时 12 项全缺 · complete=false",
        sink_title="记录落点 · 本地存储域",
        sink_chip="本地 · 不联网",
        id_label="classification_id",
        id_note="= hs_ + sha256(描述)[:12]",
        sink_note="原 CSV / JSON 不改",
    ),
    "en": dict(
        kicker="DeepSeek Harness plugin · HS candidates",
        value=["One description → three HS codes;",
               "and every missing element listed."],
        sub="Public keyword table + GIR basis; local, no network.",
        meta="7 tools · TARIFF_VERSION 2026.1 · R1 local write only",
        foot="Apache-2.0 · PerryLink DSH plugin family",
        rec_title="Record · hs_classify",
        rec_chip="R1 local write",
        ver_chip="2026.1",
        desc_label="desc",
        conf_label="confidence",
        rec_foot="Confidence ranks candidates (0.90 / 0.75 / 0.60), "
                 "not a probability · rank 1 uses GIR 1 + heading text",
        elements_title="12-element completeness",
        elements_chip="missing 12",
        elements_foot="Description only leaves all 12 missing · "
                      "complete=false",
        sink_title="Record sink · local store",
        sink_chip="local · offline",
        id_label="classification_id",
        id_note="= hs_ + sha256(description)[:12]",
        sink_note="inputs untouched",
    ),
}


def hero(lang: str, skin: str) -> None:
    s = SKIN[skin]
    H = HERO[lang]
    W, HT = 1440, 576
    img = gradient(W, HT, s["bg_from"], s["bg_to"])
    img = glow(img, 1180, 30, 420, hx(s["accent"]),
               24 if skin == "light" else 38)
    img = glow(img, 90, 580, 300, hx(s["glow2"]),
               10 if skin == "light" else 16)

    d = ImageDraw.Draw(img)
    m = 64
    col_w = 596

    # ---- left column: kicker / title / value / sub / meta / footer ----------
    pill(img, (m, 54), H["kicker"], s, size=17)
    d = ImageDraw.Draw(img)

    title = "dsh-hs-candidate"
    title_size = fit(title, "mono_bold", col_w, 58, 48)
    d.text((m - 2, 116), title, font=font(title_size, "mono_bold"),
           fill=hx(s["text"]))

    value_size = fit_lines(H["value"], "cjk_bold", col_w - 6, 40, 32)
    for i, line in enumerate(H["value"]):
        require_w(line, value_size, "cjk_bold", col_w, "hero value")
        d.text((m, 212 + i * 56), line, font=font(value_size, "cjk_bold"),
               fill=hx(s["text"]))

    sub_size = fit(H["sub"], "cjk", col_w - 6, 20, 17)
    require_w(H["sub"], sub_size, "cjk", col_w, "hero sub")
    d.text((m + 1, 338), H["sub"], font=font(sub_size, "cjk"),
           fill=hx(s["sub"]))

    meta_size = fit(H["meta"], "cjk", col_w - 6, 17, 15)
    require_w(H["meta"], meta_size, "cjk", col_w, "hero meta")
    require_w(H["foot"], 16, "cjk", col_w, "hero footer")
    d.text((m + 1, 410), H["meta"], font=font(meta_size, "cjk"),
           fill=hx(s["faint"]))
    d.line([m + 1, 462, m + col_w - 4, 462], fill=hx(s["grid"]), width=2)
    d.text((m + 1, 480), H["foot"], font=font(16, "cjk"),
           fill=hx(s["faint"]))

    # ---- right 1: the record, with the ranked Top-3 -------------------------
    img = card(img, (700, 38, 1376, 312), s)
    d = ImageDraw.Draw(img)
    d.text((724, 58), H["rec_title"], font=font(16.5, "cjk_bold"),
           fill=hx(s["accent"]))
    require_w(H["rec_title"], 16.5, "cjk_bold", 260, "record title")
    w_r1 = measure(H["rec_chip"], 11, "cjk_bold") + 20
    w_ver = measure(H["ver_chip"], 11, "cjk_bold") + 20
    chip(img, (1352 - w_r1, 58), H["rec_chip"], s["accent"], s["pill"],
         size=11)
    chip(img, (1352 - w_r1 - 8 - w_ver, 58), H["ver_chip"], s["sub"],
         s["band"], size=11)
    d = ImageDraw.Draw(img)

    require_w(H["desc_label"], 11, "cjk", 40, "desc label")
    d.text((724, 88), H["desc_label"], font=font(11, "cjk"),
           fill=hx(s["faint"]))
    desc_x = 724 + measure(H["desc_label"], 11, "cjk") + 8
    require_w(f'"{DESCRIPTION}"', 12.5, "mono", 1352 - desc_x, "description")
    d.text((desc_x, 88), f'"{DESCRIPTION}"', font=font(12.5, "mono"),
           fill=hx(s["sub"]))
    d.text((1150, 88), H["conf_label"], font=font(11, "cjk"),
           fill=hx(s["faint"]))

    for i, (code, desc, conf, gir) in enumerate(CANDIDATES):
        y = 112 + i * 58
        badge_fill = s["accent"] if i == 0 else s["band"]
        d.rounded_rectangle([724, y + 10, 754, y + 40], radius=10,
                            fill=hx(badge_fill))
        d.text((739, y + 25), str(i + 1), font=font(14, "mono_bold"),
               fill=hx(s["on_accent"] if i == 0 else s["sub"]),
               anchor="mm")
        d.text((766, y + 16), code, font=font(22, "mono_bold"),
               fill=hx(s["text"]))
        require_w(desc, 11.5, "cjk", 245, "candidate description")
        d.text((880, y + 18), desc, font=font(11.5, "cjk"),
               fill=hx(s["sub"]))
        require_w(gir, 11, "cjk", 250, "GIR basis")
        d.text((880, y + 38), gir, font=font(11, "cjk"),
               fill=hx(s["faint"]))

        d.rounded_rectangle([1150, y + 25, 1290, y + 32], radius=3,
                            fill=hx(s["band"]))
        d.rounded_rectangle([1150, y + 25, 1150 + int(140 * conf), y + 32],
                            radius=3, fill=hx(s["accent"]))
        d.text((1300, y + 21), f"{conf:.2f}", font=font(12.5, "mono_bold"),
               fill=hx(s["accent"]))
        if i < 2:
            d.line([724, y + 57, 1352, y + 57], fill=hx(s["grid"]), width=1)

    require_w(H["rec_foot"], 11, "cjk", 628, "record footer")
    d.text((724, 292), H["rec_foot"], font=font(11, "cjk"),
           fill=hx(s["sub"]))

    # ---- right 2: the 12-element grid, all missing --------------------------
    img = card(img, (700, 324, 1376, 452), s)
    d = ImageDraw.Draw(img)
    d.text((724, 336), H["elements_title"], font=font(13.5, "cjk_bold"),
           fill=hx(s["accent"]))
    w_e = measure(H["elements_chip"], 11, "cjk_bold") + 18
    chip(img, (1352 - w_e, 336), H["elements_chip"], s["mark"], s["mark_bg"],
         size=11)
    d = ImageDraw.Draw(img)

    cw, ch, gx, gy = 99, 26, 6, 4
    for i, key in enumerate(ELEMENTS):
        col, row = i % 6, i // 6
        x = 724 + col * (cw + gx)
        y = 364 + row * (ch + gy)
        d.rounded_rectangle([x, y, x + cw, y + ch], radius=8,
                            fill=hx(s["mark_bg"]))
        dash_rect(d, (x, y, x + cw, y + ch), s["mark"], width=1, dash=5,
                  gap=4)
        require_w(key, 11, "mono", cw - 12, "element key")
        d.text((x + cw / 2, y + ch / 2), key, font=font(11, "mono"),
               fill=hx(s["sub"]), anchor="mm")

    require_w(H["elements_foot"], 11, "cjk", 628, "elements footer")
    d.text((724, 430), H["elements_foot"], font=font(11, "cjk"),
           fill=hx(s["mark"]))

    # ---- right 3: the record sink ------------------------------------------
    img = card(img, (700, 460, 1376, 560), s, radius=20, shadow=18)
    d = ImageDraw.Draw(img)
    d.text((724, 476), H["sink_title"], font=font(13.5, "cjk_bold"),
           fill=hx(s["accent"]))
    require_w(H["sink_title"], 13.5, "cjk_bold", 300, "sink title")
    chip(img, (1352, 474), H["sink_chip"], s["accent2"], s["band"],
         size=11, height=21, anchor_right=True)
    d = ImageDraw.Draw(img)

    id_y = 508
    d.text((724, id_y + 5), H["id_label"], font=font(11, "mono"),
           fill=hx(s["faint"]))
    id_x = 724 + measure(H["id_label"], 11, "mono") + 10
    d.text((id_x, id_y), CLASSIFICATION_ID, font=font(16, "mono_bold"),
           fill=hx(s["text"]))
    id_end = id_x + measure(CLASSIFICATION_ID, 16, "mono_bold")
    require_w(H["id_note"], 11, "cjk", 1352 - id_end - 10, "id note")
    d.text((id_end + 10, id_y + 5), H["id_note"], font=font(11, "cjk"),
           fill=hx(s["faint"]))

    path = "$DSH_HOME/storages/hs/classifications"
    require_w(path, 11, "mono", 560, "storage path")
    d.text((724, 536), path, font=font(11, "mono"), fill=hx(s["sub"]))
    require_w(H["sink_note"], 11, "cjk", 250, "sink note")
    d.text((1352, 536), H["sink_note"], font=font(11, "cjk"),
           fill=hx(s["accent2"]), anchor="ra")

    name = f"dsh-hs-candidate-hero-{lang}-{skin}.webp"
    img.save(os.path.join(OUT, name), "WEBP", quality=92, method=6)
    print(f"wrote {name} ({W}x{HT})")


# --------------------------------------------------------------------------- flow
FLOW = {
    "light": dict(
        bg_from="#f9f6fd", bg_to="#e4eaf8",
        panel="#ffffff", edge="#e6e2ef", band="#f5f2fb",
        text="#141419", sub="#4d5261", faint="#8f94a4",
        accent="#4B67B4", accent2="#16a34a", mark="#b45309",
        rule="#dcd8ea", chip="#ece7f9",
        shadow="0.10",
    ),
    "dark": dict(
        bg_from="#131a2a", bg_to="#0c1016",
        panel="#1b2231", edge="#2e374b", band="#202839",
        text="#f0f3f9", sub="#a8b1c4", faint="#737b8d",
        accent="#8496f5", accent2="#3fb950", mark="#d9a441",
        rule="#2b3348", chip="#242d42",
        shadow="0.45",
    ),
}

FONT_CSS_CJK = ("'Microsoft YaHei','PingFang SC','Noto Sans CJK SC',"
                "'Source Han Sans SC',sans-serif")
FONT_CSS_MONO = ("'Consolas','SFMono-Regular','Menlo',ui-monospace,monospace")

# The five real CANDIDATES entries in src/core/hs.ts, in table order.
# `hit` marks the two this sample's search text matches.
BRANCHES = [
    ("3926.90", "塑料", "plastic · polymer · resin", True),
    ("7326.90", "钢铁", "steel · iron · metal", False),
    ("8501.10", "电机", "motor · generator", True),
    ("6204.62", "棉裤", "garment · trousers · cotton", False),
    ("8471.30", "便携电脑", "laptop · computer · portable", False),
]

RANK = [
    ("1", "3926.90", 0.90, "Other articles of plastics",
     "GIR 1 + heading text"),
    ("2", "8501.10", 0.75, "Motors of output <= 37.5 W",
     "GIR 1 fallback; verify with GIR 3/6"),
    ("3", "7326.90", 0.60, "Other articles of iron or steel",
     "GIR 1 fallback; verify with GIR 3/6"),
]

BENCH = [
    ("hs_code_check", "84713000 ✓ · 9999.00 保留章"),
    ("hs_rvc_check", "50% ≥ 40 · qualifies"),
    ("hs_rvc_report", "30 · 60 · 60 三口径"),
    ("hs_lookup", "公开表内 ≤ 5 行"),
]


class Svg:
    """Tiny SVG writer that measures every label before it is emitted."""

    def __init__(self) -> None:
        self.parts: list[str] = []
        self.overflows: list[str] = []

    def add(self, markup: str) -> None:
        self.parts.append(markup)

    def text(self, x: float, y: float, content: str, size: float, fill: str,
             *, anchor: str = "start", weight: int | None = None,
             mono: bool = False, max_w: float | None = None,
             opacity: float | None = None) -> None:
        kind = ("mono" if mono else "cjk") + ("_bold" if weight else "")
        if mono and weight:
            kind = "mono_bold"
        if max_w is not None:
            w = measure(content, size, kind)
            if w > max_w + 0.4:
                self.overflows.append(
                    f"{content!r} needs {w:.1f}px > {max_w}px")
        family = FONT_CSS_MONO if mono else FONT_CSS_CJK
        attrs = [f'x="{x}"', f'y="{y}"', f'fill="{fill}"',
                 f'font-family="{family}"', f'font-size="{size}"']
        if anchor != "start":
            attrs.append(f'text-anchor="{anchor}"')
        if weight:
            attrs.append(f'font-weight="{weight}"')
        if opacity is not None:
            attrs.append(f'opacity="{opacity}"')
        self.add(f'<text {" ".join(attrs)}>{escape(content)}</text>')

    def rect(self, x: float, y: float, w: float, h: float, *, fill: str,
             rx: float = 0, stroke: str | None = None, sw: float = 1.5,
             shadow: bool = False, dash: str | None = None,
             opacity: float | None = None) -> None:
        attrs = [f'x="{x}"', f'y="{y}"', f'width="{w}"', f'height="{h}"']
        if rx:
            attrs.append(f'rx="{rx}"')
        attrs.append(f'fill="{fill}"')
        if stroke:
            attrs.append(f'stroke="{stroke}"')
            attrs.append(f'stroke-width="{sw}"')
        if dash:
            attrs.append(f'stroke-dasharray="{dash}"')
        if opacity is not None:
            attrs.append(f'opacity="{opacity}"')
        if shadow:
            attrs.append('filter="url(#soft)"')
        self.add(f'<rect {" ".join(attrs)}/>')

    def line(self, x1: float, y1: float, x2: float, y2: float, *, stroke: str,
             sw: float = 1.5, dash: str | None = None,
             marker: str | None = None, opacity: float | None = None) -> None:
        attrs = [f'x1="{x1}"', f'y1="{y1}"', f'x2="{x2}"', f'y2="{y2}"',
                 f'stroke="{stroke}"', f'stroke-width="{sw}"']
        if dash:
            attrs.append(f'stroke-dasharray="{dash}"')
        if marker:
            attrs.append(f'marker-end="url(#{marker})"')
        if opacity is not None:
            attrs.append(f'opacity="{opacity}"')
        self.add(f'<line {" ".join(attrs)}/>')

    def dot(self, cx: float, cy: float, r: float, fill: str,
            opacity: float | None = None) -> None:
        extra = '' if opacity is None else f' opacity="{opacity}"'
        self.add(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{fill}"{extra}/>')

    def chip(self, x: float, y: float, label: str, fg: str, bg: str,
             *, size: float = 11, pad: float = 8, height: float = 18,
             mono: bool = False, weight: int | None = None,
             anchor_right: bool = False) -> float:
        kind = ("mono" if mono else "cjk") + ("_bold" if weight else "")
        if mono and weight:
            kind = "mono_bold"
        w = measure(label, size, kind) + pad * 2
        bx = x - w if anchor_right else x
        self.rect(bx, y, w, height, fill=bg, rx=height / 2)
        self.text(bx + pad, y + height / 2 + size * 0.34, label, size, fg,
                  weight=weight, mono=mono)
        return w

    def svg(self, w: int, h: int, label: str) -> str:
        head = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" '
                f'height="{h}" viewBox="0 0 {w} {h}" role="img" '
                f'aria-label="{escape(label)}">')
        return "\n".join([head, *self.parts, "</svg>"]) + "\n"


def flow_svg(skin: str) -> str:
    s = FLOW[skin]
    W, H = 1100, 660
    v = Svg()

    v.add("<defs>")
    v.add(f'<linearGradient id="bg" x1="0" y1="0" x2="0.3" y2="1">'
          f'<stop offset="0" stop-color="{s["bg_from"]}"/>'
          f'<stop offset="1" stop-color="{s["bg_to"]}"/></linearGradient>')
    v.add(f'<filter id="soft" x="-30%" y="-30%" width="160%" height="170%">'
          f'<feDropShadow dx="0" dy="7" stdDeviation="9" '
          f'flood-color="#16122c" flood-opacity="{s["shadow"]}"/></filter>')
    v.add('<marker id="arr" viewBox="0 0 10 10" refX="9" refY="5" '
          'markerWidth="5.6" markerHeight="5.6" orient="auto-start-reverse">'
          f'<path d="M0 0 L10 5 L0 10 z" fill="{s["accent"]}"/></marker>')
    v.add("</defs>")
    v.add(f'<rect width="{W}" height="{H}" fill="url(#bg)"/>')

    # ---- header -------------------------------------------------------------
    v.text(44, 52, "dsh-hs-candidate", 24, s["text"], weight=700, mono=True,
           max_w=250)
    v.text(274, 52, "关键词分支 → Top-3 短名单", 23, s["text"], weight=700,
           max_w=540)
    v.chip(1056, 34, "TARIFF_VERSION 2026.1 · 公开表 5 条", s["accent"],
           s["band"], size=11.5, pad=11, height=24, anchor_right=True)
    v.text(44, 84,
           "一条描述进入关键词表：命中项按表序在前，不足 3 条再从表序补位；"
           "候选、缺项与税则版本一起写成一条本地记录。",
           14, s["sub"], max_w=1012)
    v.line(44, 100, 1056, 100, stroke=s["rule"], sw=1)

    v.text(280, 116, "公开关键词表 · 5 条真实条目（另有 1 条兜底不入候选）",
           11, s["faint"], max_w=372)

    # ---- tree: root, spine, five keyword branches ---------------------------
    v.line(246, 154, 246, 402, stroke=s["rule"], sw=1.4)
    v.line(228, 282, 246, 282, stroke=s["accent"], sw=1.8)

    for i, (code, label, keys, hit) in enumerate(BRANCHES):
        cy = 154 + i * 62
        v.line(246, cy, 277 if hit else 280, cy,
               stroke=s["accent"] if hit else s["rule"],
               sw=1.9 if hit else 1.3,
               marker="arr" if hit else None)
        v.dot(246, cy, 3.2, s["accent"] if hit else s["faint"])
        y = cy - 26
        v.rect(280, y, 290, 52, fill=s["panel"], rx=16,
               stroke=s["accent"] if hit else s["edge"],
               sw=2 if hit else 1.4)
        v.text(294, y + 23, code, 16,
               s["accent"] if hit else s["text"], weight=700, mono=True,
               max_w=90)
        code_w = measure(code, 16, "mono_bold")
        v.text(294 + code_w + 8, y + 23, label, 13,
               s["accent"] if hit else s["sub"], weight=700, max_w=60)
        v.text(294, y + 42, keys, 11, s["faint"], mono=True, max_w=262)
        v.chip(558, y + 8, "命中" if hit else "未命中",
               s["accent"] if hit else s["faint"],
               s["chip"] if hit else s["band"],
               size=11, pad=8, height=19, anchor_right=True)

    # root card sits on the spine; drawn after the rails so it covers them
    v.rect(44, 218, 184, 130, fill=s["panel"], rx=20, stroke=s["edge"],
           sw=1.5, shadow=True)
    v.text(60, 242, "输入 · 检索文本", 13, s["accent"], weight=700, max_w=152)
    v.text(60, 266, "descriptions.csv", 11, s["text"], mono=True, max_w=112)
    v.text(208, 266, "20 行", 11, s["faint"], anchor="end", max_w=40)
    v.text(60, 286, "elements.json", 11, s["text"], mono=True, max_w=112)
    v.text(208, 286, "可选", 11, s["faint"], anchor="end", max_w=30)
    v.line(60, 298, 212, 298, stroke=s["rule"], sw=1)
    v.text(60, 310, "描述 + 要素值拼接", 11, s["sub"], max_w=160)
    v.text(60, 328, "12 键可并入 → 关键词表", 11, s["accent"], weight=700,
           max_w=160)

    # ---- right: the Top-3 shortlist ----------------------------------------
    v.rect(596, 112, 460, 322, fill=s["panel"], rx=20, stroke=s["edge"],
           sw=1.5, shadow=True)
    v.text(612, 136, "Top-3 短名单", 13, s["accent"], weight=700, max_w=230)
    v.chip(1040, 130, "置信度仅排序", s["sub"], s["band"], size=11, pad=8,
           height=19, anchor_right=True)
    v.text(612, 160, "示例", 11, s["faint"], max_w=40)
    v.text(642, 160, DESCRIPTION, 11, s["sub"], mono=True, max_w=300)
    v.text(858, 160, "· 20 条各一份", 11, s["faint"], max_w=150)

    for i, (rank, code, conf, desc, gir) in enumerate(RANK):
        y = 178 + i * 60
        v.rect(612, y + 10, 26, 26, fill=s["band"], rx=8)
        v.text(625, y + 28, rank, 13, s["accent"], weight=700, mono=True,
               anchor="middle", max_w=20)
        v.text(646, y + 26, code, 17.5, s["text"], weight=700, mono=True,
               max_w=90)
        v.text(736, y + 20, desc, 11.5, s["sub"], max_w=180)
        v.text(736, y + 40, gir, 11, s["faint"], max_w=180)
        v.rect(928, y + 20, 80, 6, fill=s["band"], rx=3)
        v.rect(928, y + 20, 80 * conf, 6, fill=s["accent"], rx=3)
        v.text(1044, y + 27, f"{conf:.2f}", 11, s["accent"], weight=700,
               mono=True, anchor="end", max_w=40)

    v.text(612, 376, "命中 2 条 → 第 3 位按表序补齐 7326.90", 11, s["mark"],
           weight=700, max_w=432)
    v.text(612, 394,
           "首位 GIR 1 + 品目条文；其余 GIR 1 兜底，按 GIR 3/6 复核",
           11, s["sub"], max_w=432)
    v.text(612, 412, "置信度 0.9 / 0.75 / 0.6 是排序提示，不是概率",
           11, s["faint"], max_w=432)

    # ---- bottom left: the record that classify writes -----------------------
    v.rect(44, 448, 652, 144, fill=s["panel"], rx=20, stroke=s["edge"],
           sw=1.5, shadow=True)
    v.text(62, 470, "归类记录 · classifications", 13, s["accent"], weight=700,
           max_w=280)
    v.chip(680, 464, "R1 本地写", s["accent"], s["chip"], size=11, pad=9,
           height=20, anchor_right=True)
    v.line(370, 486, 370, 560, stroke=s["rule"], sw=1)
    v.text(62, 490, "classification_id", 11, s["faint"], mono=True, max_w=150)
    v.text(386, 490, "top3[3]", 11, s["faint"], mono=True, max_w=90)
    v.text(62, 510, CLASSIFICATION_ID, 13, s["text"], weight=700, mono=True,
           max_w=150)
    v.text(386, 510, "3926.90 · 8501.10 · 7326.90", 13, s["text"], mono=True,
           max_w=290)
    v.text(62, 534, "missing_elements", 11, s["faint"], mono=True, max_w=150)
    v.text(386, 534, "tariff_version", 11, s["faint"], mono=True, max_w=120)
    v.text(62, 554, "12", 13, s["mark"], weight=700, mono=True, max_w=20)
    v.text(86, 554, "· complete=false", 11, s["sub"], max_w=120)
    v.text(184, 554, "仅传描述", 11, s["mark"], max_w=60)
    v.text(386, 554, "2026.1", 13, s["text"], weight=700, mono=True,
           max_w=60)
    v.text(62, 578, "写入 $DSH_HOME/storages/hs/ · 原 CSV / JSON 不改", 11,
           s["faint"], max_w=500)

    # ---- bottom right: the read-only bench ---------------------------------
    v.rect(712, 448, 344, 144, fill=s["panel"], rx=20, stroke=s["edge"],
           sw=1.5, shadow=True)
    v.text(730, 470, "R0 校验台 · 只读旁路", 13, s["accent"], weight=700,
           max_w=250)
    v.chip(1040, 464, "不写记录", s["faint"], s["band"], size=11, pad=8,
           height=19, anchor_right=True)
    for i, (tool, result) in enumerate(BENCH):
        y = 496 + i * 24
        v.text(730, y, tool, 11.5, s["text"], weight=700, mono=True,
               max_w=102)
        v.text(840, y, result, 11, s["sub"], max_w=200)

    # ---- footer -------------------------------------------------------------
    v.line(44, 608, 1056, 608, stroke=s["rule"], sw=1)
    v.text(44, 626,
           "PerryLink DSH plugin family · Apache-2.0 · 配图由 "
           "scripts/gen-readme-assets.py 生成",
           11, s["faint"], max_w=700)
    v.text(1056, 626, "公开表 5 条 + 兜底 1 条 · 本地，不联网", 11,
           s["faint"], anchor="end", max_w=260)

    if v.overflows:
        raise SystemExit("FATAL: SVG label overflow:\n  " +
                         "\n  ".join(v.overflows))
    return v.svg(W, H, "dsh-hs-candidate 结构图：描述与要素值进入五条公开关键词"
                       "分支，塑料与电机两条命中，第三位按表序补齐；Top-3 短名单"
                       "带 GIR 依据，记录含 12 项缺失与税则 2026.1，写入本地"
                       "存储域；R0 校验台为只读旁路")


def main() -> None:
    os.makedirs(OUT, exist_ok=True)
    for skin in ("light", "dark"):
        for lang in ("zh", "en"):
            hero(lang, skin)
        name = f"dsh-hs-candidate-flow-v5-{skin}.svg"
        with open(os.path.join(OUT, name), "w", encoding="utf-8",
                  newline="\n") as fh:
            fh.write(flow_svg(skin))
        print(f"wrote {name} (1100x660)")


if __name__ == "__main__":
    main()
