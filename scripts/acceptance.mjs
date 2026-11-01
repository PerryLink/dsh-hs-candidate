import{mkdirSync,writeFileSync}from'node:fs';import{createHash}from'node:crypto';import{createTools}from'../lib/plugin/tools.js'
class T{map=new Map();get(k){return this.map.get(k)};entries(){return this.map.entries()};get size(){return this.map.size};async put(k,v){this.map.set(k,v)}}
const desc=['plastic housing','steel bracket','electric motor','cotton garment','laptop computer'];const b=Object.fromEntries(createTools({classifications:new T()}).map(t=>[t.name,t]));let top=0;for(let i=0;i<20;i++){const r=await b['hs.classify'].execute({description:desc[i%5]},{callId:'a'});if(r.top3.length===3)top++}const el=await b['hs.elements'].execute({elements:{}},{callId:'a'});const v=await b['hs.tariff_version'].execute({},{callId:'a'})
const rvcTools=createTools({classifications:new T()});const rvc=await rvcTools.find(t=>t.name==='hs.rvc_check').execute({value_cents:10000,materials:[{origin:'CN',value_cents:5000},{origin:'US',value_cents:5000}]},{callId:'a'});const codeTools=createTools({recs:new T(),baseDir:'/tmp/hs-code-acc'});const cbt=Object.fromEntries(codeTools.map(t=>[t.name,t]));const code=await cbt['hs.code_check'].execute({code:'8471.30'},{callId:'a'});const badCode=await cbt['hs.code_check'].execute({code:'9999.00'},{callId:'a'});
const ms=[{i:'SKU-13-A01',m:'Top3 候选（20）',t:'20/20',a:top,p:top===20},{i:'SKU-13-A02',m:'缺失要素提示',t:'>=1',a:el.missing.length,p:el.missing.length>0},{i:'SKU-13-A03',m:'必填要素',t:'12',a:v.elements.length,p:v.elements.length===12},{i:'SKU-13-A04',m:'税则版本',t:'set',a:v.version?1:0,p:Boolean(v.version)},{i:'SKU-13-A05',m:'RVC 简单比值',t:'50',a:rvc.rvc_pct,p:rvc.rvc_pct===50},{i:'SKU-13-A06',m:'HS 编码结构',t:'1/1',a:code.valid?1:0,p:code.valid===true&&badCode.reason==='E_HS_CODE_CHAPTER_RESERVED'}];const r={run_id:`sku13-${Date.now()}`,scope:'SKU-13-S1',status:'partial',counted:false,note:'synthetic descriptions; user-approved public/synthetic; 0 real declarations',metrics:ms,pass:ms.every(x=>x.p)};const dir=`evidence/${r.run_id}`;mkdirSync(dir,{recursive:true});const s=JSON.stringify(r,null,2)+'\n';writeFileSync(`${dir}/result.json`,s);const h=createHash('sha256').update(s).digest('hex');writeFileSync('ACCEPTANCE.csv','req_id,metric,threshold,actual,script,evidence_sha256,pass\n'+ms.map(x=>`${x.i},${x.m},${x.t},${x.a},scripts/acceptance.mjs,${h},${x.p}`).join('\n')+'\n');if(!r.pass)process.exit(1);console.log('acceptance ok')


// Normalize the public-only acceptance schema: source + counted=false.
{
  const fs = await import('node:fs')
  const file = 'ACCEPTANCE.csv'
  const lines = fs.readFileSync(file, 'utf8').trim().split('\n')
  if (!lines[0].includes('source,counted')) {
    lines[0] += ',source,counted'
    for (let i = 1; i < lines.length; i += 1) lines[i] += ',public/synthetic,false'
    fs.writeFileSync(file, lines.join('\n') + '\n')
  }
}
