import test from 'node:test'
import assert from 'node:assert/strict'
import { createTools } from '../lib/plugin/tools.js'

class T { map = new Map(); get(k){return this.map.get(k)}; entries(){return this.map.entries()}; get size(){return this.map.size}; async put(k,v){this.map.set(k,v)} }
const tools = Object.fromEntries(createTools({ recs: new T(), baseDir: '/tmp/hs-code' }).map((t) => [t.name, t]))
const exec = { callId: 'hs' }

test('6/8/10 digit codes are accepted with dot-insensitive normalisation', async () => {
  const six = await tools['hs.code_check'].execute({ code: '8471.30' }, exec)
  assert.equal(six.valid, true)
  assert.equal(six.normalized, '847130')
  assert.equal(six.chapter, '84')
  assert.equal(six.subheading, '847130')
  const eight = await tools['hs.code_check'].execute({ code: '84713000' }, exec)
  assert.equal(eight.valid, true)
  const ten = await tools['hs.code_check'].execute({ code: '8471 30 00 90' }, exec)
  assert.equal(ten.valid, true)
  assert.equal(ten.normalized, '8471300090')
})

test('bad length, letters and reserved chapters get distinct reasons', async () => {
  assert.equal((await tools['hs.code_check'].execute({ code: '84713' }, exec)).reason, 'E_HS_CODE_LENGTH')
  assert.equal((await tools['hs.code_check'].execute({ code: 'ABCDEF' }, exec)).reason, 'E_HS_CODE_FORMAT')
  assert.equal((await tools['hs.code_check'].execute({ code: '0000' }, exec)).reason, 'E_HS_CODE_CHAPTER_RESERVED')
  assert.equal((await tools['hs.code_check'].execute({ code: '9999.00' }, exec)).reason, 'E_HS_CODE_CHAPTER_RESERVED')
})

test('chapter 97 is the last valid chapter', async () => {
  const ok = await tools['hs.code_check'].execute({ code: '9701.10' }, exec)
  assert.equal(ok.valid, true)
  const reserved = await tools['hs.code_check'].execute({ code: '9801.00' }, exec)
  assert.equal(reserved.valid, false)
  assert.equal(reserved.reason, 'E_HS_CODE_CHAPTER_RESERVED')
})
