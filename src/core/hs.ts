export type HsErrorCode='E_HS_DESCRIPTION_MISSING'|'E_HS_TARIFF_VERSION'|'E_HS_ELEMENT_INVALID'|'E_HS_CODE_FORMAT'|'E_HS_CODE_LENGTH'|'E_HS_CODE_CHAPTER_RESERVED'
export class HsError extends Error{readonly code:HsErrorCode;constructor(code:HsErrorCode,message:string){super(`${code}: ${message}`);this.name='HsError';this.code=code}}
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
export function candidates(description:string,elements?:Record<string,unknown>){if(!description.trim())throw new HsError('E_HS_DESCRIPTION_MISSING','description required');const text=`${description} ${Object.values(elements??{}).join(' ')}`;const hits=CANDIDATES.filter(c=>c.keywords.test(text)).filter(c=>c.code!=='9999.00');const ordered=[...hits,...CANDIDATES.filter(c=>!hits.includes(c))].slice(0,3);return ordered.map((c,i)=>({code:c.code,description:c.description,confidence:Math.max(0.5,0.9-i*0.15),gir_basis:i===0?'GIR 1 + heading text':'GIR 1 fallback; verify with GIR 3/6'}))}

export interface HsCodeResult {
  code: string
  normalized: string
  valid: boolean
  chapter?: string
  heading?: string
  subheading?: string
  reason?: string
}
/**
 * Structural check of an HS 2022 code: 2/4/6/8/10 digits (6 is the international subheading,
 * 8/10 are national extensions). Chapters run 01-97; 98/99 are reserved for national use.
 */
export function hsCodeCheck(raw: string): HsCodeResult {
  const code = raw.trim()
  const digits = code.replace(/[.\s]/g, '')
  if (!digits) return { code, normalized: '', valid: false, reason: 'E_HS_CODE_FORMAT' }
  if (!/^\d+$/.test(digits)) return { code, normalized: digits, valid: false, reason: 'E_HS_CODE_FORMAT' }
  if (![2, 4, 6, 8, 10].includes(digits.length)) return { code, normalized: digits, valid: false, reason: 'E_HS_CODE_LENGTH' }
  const chapter = digits.slice(0, 2)
  const chapterNumber = Number(chapter)
  const base = { code, normalized: digits, valid: true, chapter, heading: digits.slice(0, 4), subheading: digits.length >= 6 ? digits.slice(0, 6) : undefined }
  if (chapterNumber === 0 || chapterNumber > 99) return { ...base, valid: false, reason: 'E_HS_CODE_CHAPTER_RESERVED' }
  if (chapterNumber > 97) return { ...base, valid: false, reason: 'E_HS_CODE_CHAPTER_RESERVED' }
  return base
}
