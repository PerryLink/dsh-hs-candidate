import test from 'node:test'
import assert from 'node:assert/strict'
import { rvcReport } from '../lib/core/hs.js'
import { createTools } from '../lib/plugin/tools.js'

class T { map = new Map(); get(k){return this.map.get(k)}; entries(){return this.map.entries()}; get size(){return this.map.size}; async put(k,v){this.map.set(k,v)} }
const tools = Object.fromEntries(createTools({ recs: new T(), baseDir: '/tmp/hs-rvc' }).map((t) => [t.name, t]))
const exec = { callId: 'rvc' }

test('the three formulas agree on a fully domestic good', async () => {
  const r = await tools['hs.rvc_report'].execute({ fob_cents: 10000, non_originating_cents: 0, domestic_value_cents: 10000 }, exec)
  assert.equal(r.methods.length, 3)
  for (const m of r.methods) assert.equal(m.rvc_pct, 100)
  assert.equal(r.meets_threshold, true)
})

test('build-down and build-up diverge when labour and overhead are declared', async () => {
  const r = await tools['hs.rvc_report'].execute({ fob_cents: 10000, non_originating_cents: 4000, domestic_value_cents: 3000, labour_overhead_cents: 3000 }, exec)
  const by = Object.fromEntries(r.methods.map((m) => [m.method, m.rvc_pct]))
  assert.equal(by.simple_ratio, 30)
  assert.equal(by.build_down, 60)
  assert.equal(by.build_up, 60)
})

test('the threshold check passes when any method clears it', async () => {
  const below = await tools['hs.rvc_report'].execute({ fob_cents: 10000, non_originating_cents: 9000, domestic_value_cents: 1000, threshold_pct: 50 }, exec)
  assert.equal(below.meets_threshold, false)
  const above = await tools['hs.rvc_report'].execute({ fob_cents: 10000, non_originating_cents: 2000, domestic_value_cents: 8000, threshold_pct: 50 }, exec)
  assert.equal(above.meets_threshold, true)
})

test('a zero FOB is rejected and negative values are reported', () => {
  const zero = rvcReport({ fob_cents: 0, non_originating_cents: 0, domestic_value_cents: 0 })
  assert.deepEqual(zero.methods, [])
  assert.ok(zero.issues.includes('E_HS_RVC_FOB'))
  const negative = rvcReport({ fob_cents: 100, non_originating_cents: -1, domestic_value_cents: 50 })
  assert.ok(negative.issues.includes('E_HS_RVC_NEGATIVE'))
})
