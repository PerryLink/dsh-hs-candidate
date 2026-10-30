import type{Context}from'@deepseek-ai/cordis';import{createTools}from'./tools.js';import{openHs}from'./storage.js'
export const name='dsh-hs-candidate';export const inject=['tools','storageDomain']
export async function apply(ctx:Context):Promise<void>{const classifications=await openHs(ctx);for(const t of createTools({classifications}))ctx.tools.register(t)}
