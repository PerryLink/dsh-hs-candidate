import{defineDomain,domainTable}from'@deepseek-ai/dsh-storage-domain';import type{Context}from'@deepseek-ai/cordis';import{z}from'zod'
const rec=z.object({classification_id:z.string(),description:z.string(),tariff_version:z.string(),top3:z.array(z.object({code:z.string(),description:z.string(),confidence:z.number(),gir_basis:z.string()})),missing_elements:z.array(z.string()),created_at:z.string()})
export type Rec=z.infer<typeof rec>;export type Table<T>={get(k:string):T|undefined;entries():IterableIterator<[string,T]>;size:number;put(k:string,v:T):Promise<void>}
export const hsSpec=defineDomain({name:'hs',version:1,tables:{classifications:domainTable<string,Rec>(rec)}})
export async function openHs(ctx:Context){const d=await ctx.storageDomain.open(hsSpec);ctx.effect(()=>()=>d.close(),'dsh-hs-candidate.domainClose');return d.table('classifications') as Table<Rec>}
