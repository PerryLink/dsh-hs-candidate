export type HsErrorCode='E_HS_DESCRIPTION_MISSING'|'E_HS_TARIFF_VERSION'|'E_HS_ELEMENT_INVALID'|'E_HS_CODE_FORMAT'|'E_HS_CODE_LENGTH'|'E_HS_CODE_CHAPTER_RESERVED'|'E_HS_RVC_INVALID'
/** User-facing text for every error code: one plain sentence plus one next action. */
const HS_HUMAN:Record<HsErrorCode,{text:string;next:string}>={
 E_HS_DESCRIPTION_MISSING:{text:'产品描述是空的，没法给出候选编码',next:'用一句话写清材质、用途和功能再试'},
 E_HS_TARIFF_VERSION:{text:'税则版本不是当前支持的版本',next:'先运行 hs.tariff_version 看当前版本，再按这个版本填'},
 E_HS_ELEMENT_INVALID:{text:'12 项归类要素里有格式不对的项',next:'每一项都填非空文本，数字和单位分开写'},
 E_HS_CODE_FORMAT:{text:'这不是 HS 编码：里面有字母或符号',next:'只填数字和点，例如 8471.30'},
 E_HS_CODE_LENGTH:{text:'HS 编码位数不对',next:'用 2/4/6/8/10 位，例如 8471.30 或 84713000'},
 E_HS_CODE_CHAPTER_RESERVED:{text:'这个章节号（00 或 98/99）是保留章，不能直接归类',next:'换成 01–97 章的真实编码，或交人工复核'},
 E_HS_RVC_INVALID:{text:'RVC 计算的 FOB 金额或材料清单无效',next:'FOB 要大于 0，材料至少给一行'},
}
/** `human sentence（E_CODE）｜Next: one action` — the only text shown to end users. */
export function hsErrorMessage(code:HsErrorCode,text?:string){const h=HS_HUMAN[code];return `${text??h.text}（${code}）｜下一步：${h.next}`}
export class HsError extends Error{readonly code:HsErrorCode;constructor(code:HsErrorCode,text?:string){super(hsErrorMessage(code,text));this.name='HsError';this.code=code}}
export const TARIFF_VERSION='2026.1'
export const ELEMENTS=['product_name','material','function','use','composition','processing','packaging','brand','model','spec','origin','unit']
export const CANDIDATES=[
 {code:'3926.90',keywords:/plastic|塑料|polymer|resin/i,description:'Other articles of plastics'},
 {code:'7326.90',keywords:/steel|钢|iron|铁|metal/i,description:'Other articles of iron or steel'},
 {code:'8501.10',keywords:/motor|电机|electric motor|generator/i,description:'Motors of output <= 37.5 W'},
 {code:'6204.62',keywords:/garment|服装|trousers|pants|棉/i,description:"Women's trousers of cotton"},
 {code:'8471.30',keywords:/laptop|computer|电脑|portable/i,description:'Portable automatic data processing machines'},
 {code:'9999.00',keywords:/.*/,description:'Unclassified candidate; human review required'},
]
export function missingElements(elements:Record<string,unknown>|undefined){return ELEMENTS.filter(k=>!elements||typeof elements[k]!=='string'||!(elements[k] as string).trim())}
export function candidates(description:string,elements?:Record<string,unknown>){if(!description.trim())throw new HsError('E_HS_DESCRIPTION_MISSING');const text=`${description} ${Object.values(elements??{}).join(' ')}`;const hits=CANDIDATES.filter(c=>c.keywords.test(text)).filter(c=>c.code!=='9999.00');const ordered=[...hits,...CANDIDATES.filter(c=>!hits.includes(c))].slice(0,3);return ordered.map((c,i)=>({code:c.code,description:c.description,confidence:Math.max(0.5,0.9-i*0.15),gir_basis:i===0?'GIR 1 + heading text':'GIR 1 fallback; verify with GIR 3/6'}))}

export interface HsCodeResult {
  code: string
  normalized: string
  valid: boolean
  chapter?: string
  heading?: string
  subheading?: string
  reason?: string
  /** Plain-language version of `reason`, shown to the end user. */
  message?: string
}
/**
 * Structural check of an HS 2022 code: 2/4/6/8/10 digits (6 is the international subheading,
 * 8/10 are national extensions). Chapters run 01-97; 98/99 are reserved for national use.
 */
export function hsCodeCheck(raw: string): HsCodeResult {
  const code = raw.trim()
  const digits = code.replace(/[.\s]/g, '')
  if (!digits) return { code, normalized: '', valid: false, reason: 'E_HS_CODE_FORMAT', message: hsErrorMessage('E_HS_CODE_FORMAT') }
  if (!/^\d+$/.test(digits)) return { code, normalized: digits, valid: false, reason: 'E_HS_CODE_FORMAT', message: hsErrorMessage('E_HS_CODE_FORMAT') }
  if (![2, 4, 6, 8, 10].includes(digits.length)) return { code, normalized: digits, valid: false, reason: 'E_HS_CODE_LENGTH', message: hsErrorMessage('E_HS_CODE_LENGTH') }
  const chapter = digits.slice(0, 2)
  const chapterNumber = Number(chapter)
  const base = { code, normalized: digits, valid: true, chapter, heading: digits.slice(0, 4), subheading: digits.length >= 6 ? digits.slice(0, 6) : undefined }
  if (chapterNumber === 0 || chapterNumber > 99) return { ...base, valid: false, reason: 'E_HS_CODE_CHAPTER_RESERVED', message: hsErrorMessage('E_HS_CODE_CHAPTER_RESERVED') }
  if (chapterNumber > 97) return { ...base, valid: false, reason: 'E_HS_CODE_CHAPTER_RESERVED', message: hsErrorMessage('E_HS_CODE_CHAPTER_RESERVED') }
  return base
}

export type RvcMethod = 'simple_ratio' | 'build_down' | 'build_up'
export interface RvcInput {
  fob_cents: number
  non_originating_cents: number
  domestic_value_cents: number
  labour_overhead_cents?: number
}
export interface RvcMethodResult { method: RvcMethod; rvc_pct: number | null; reason?: string }
/**
 * Regional value content under the three formulas used in preferential rules of origin:
 * simple ratio (domestic / FOB), build-down ((FOB - non-originating) / FOB) and
 * build-up ((originating materials + labour/overhead) / FOB).
 * Clean-room from the published WTO/WCO rules-of-origin formulas; not a customs ruling.
 */
export function rvcReport(input: RvcInput): { methods: RvcMethodResult[]; fob_cents: number; issues: string[] } {
  const issues: string[] = []
  const fob = input.fob_cents
  if (!Number.isFinite(fob) || fob <= 0) {
    issues.push('E_HS_RVC_FOB')
    return { methods: [], fob_cents: fob, issues }
  }
  const pct = (numerator: number) => Math.round((numerator / fob) * 10000) / 100
  const nonOrig = Number.isFinite(input.non_originating_cents) ? input.non_originating_cents : 0
  const domestic = Number.isFinite(input.domestic_value_cents) ? input.domestic_value_cents : 0
  const labour = Number.isFinite(input.labour_overhead_cents ?? 0) ? (input.labour_overhead_cents ?? 0) : 0
  if (nonOrig < 0 || domestic < 0 || labour < 0) issues.push('E_HS_RVC_NEGATIVE')
  const methods: RvcMethodResult[] = [
    { method: 'simple_ratio', rvc_pct: pct(domestic) },
    { method: 'build_down', rvc_pct: pct(fob - nonOrig) },
    { method: 'build_up', rvc_pct: pct(domestic + labour) },
  ]
  return { methods, fob_cents: fob, issues }
}
