import test from 'node:test'
import assert from 'node:assert/strict'
import { readFileSync } from 'node:fs'
import { createTools } from '../lib/plugin/tools.js'

class T { map=new Map(); get(k){return this.map.get(k)}; entries(){return this.map.entries()}; get size(){return this.map.size}; async put(k,v){this.map.set(k,v)} }

test('public MIT HS table lookup', async () => {
  const table = JSON.parse(readFileSync('fixtures/public/mit/hs-sample.json', 'utf8'))
  const tools = createTools({ classifications: new T() })
  const lookup = tools.find((tool) => tool.name === 'hs_lookup')
  const result = await lookup.execute({ hs_table: table, query: 'horses' }, { callId: 'hs' })
  assert.ok(result.matches.length > 0)
  assert.ok(result.matches.every((row) => row.code && row.description))
})
