import test from 'node:test'
import assert from 'node:assert/strict'
import { createTools } from '../lib/plugin/tools.js'

class T {
  map = new Map()
  get(k) { return this.map.get(k) }
  entries() { return this.map.entries() }
  get size() { return this.map.size }
  async put(k, v) { this.map.set(k, v) }
}

// The model wire format only accepts names matching ^[a-zA-Z0-9_-]+$.
// A dotted name (the 0.1.x style) is rejected by the provider
// with `Invalid 'tools[N].name'` and takes the whole tools array down with it,
// so the plugin registers but no request that carries the tools can succeed.
const WIRE_NAME = /^[a-zA-Z0-9_-]+$/

const EXPECTED = [
  'hs_elements',
  'hs_classify',
  'hs_tariff_version',
  'hs_lookup',
  'hs_rvc_check',
  'hs_code_check',
  'hs_rvc_report',
]

test('every registered tool name is a valid model wire name', () => {
  const tools = createTools({ classifications: new T() })
  assert.equal(tools.length, 7)
  for (const tool of tools) {
    assert.match(tool.name, WIRE_NAME, `${tool.name} would be rejected by the provider`)
    assert.ok(!tool.name.includes('.'), `${tool.name} must not contain a dot`)
    assert.ok(tool.name.startsWith('hs_'), `${tool.name} must keep the hs_ namespace`)
  }
  const names = tools.map((tool) => tool.name)
  assert.equal(new Set(names).size, names.length, 'tool names must be unique')
  assert.deepEqual([...names].sort(), [...EXPECTED].sort())
})
