import test from 'node:test'
import assert from 'node:assert/strict'
import { createTools } from '../lib/plugin/tools.js'
class T { map=new Map(); get(k){return this.map.get(k)}; entries(){return this.map.entries()}; get size(){return this.map.size}; async put(k,v){this.map.set(k,v)} }
test('RVC simple ratio', async () => {
  const tools = createTools({ classifications: new T() })
  const rvc = tools.find((tool) => tool.name === 'hs_rvc_check')
  const result = await rvc.execute({ value_cents: 10000, materials: [{ origin: 'CN', value_cents: 5000 }, { origin: 'US', value_cents: 5000 }] }, { callId: 'rvc' })
  assert.equal(result.rvc_pct, 50)
  assert.equal(result.qualifies, true)
})
