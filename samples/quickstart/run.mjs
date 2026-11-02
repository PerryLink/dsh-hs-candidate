#!/usr/bin/env node
/**
 * dsh-hs-candidate quickstart — runs the built plugin tools over the bundled
 * synthetic product descriptions and code list. The golden file
 * `expected/result.json` is the stdout of
 * `node samples/quickstart/run.mjs --json`, so it is a real run, not hand-written.
 *
 *   node samples/quickstart/run.mjs            # human-readable summary
 *   node samples/quickstart/run.mjs --json     # the golden result on stdout
 *   node samples/quickstart/run.mjs --check    # recompute and diff against the golden file
 */
import assert from 'node:assert/strict'
import { readFile } from 'node:fs/promises'
import path from 'node:path'
import { fileURLToPath } from 'node:url'
import { createTools } from '../../lib/plugin/tools.js'

const here = path.dirname(fileURLToPath(import.meta.url))
const inputDir = path.join(here, 'input')
const expectedPath = path.join(here, 'expected', 'result.json')
const mode = process.argv.includes('--check') ? 'check' : process.argv.includes('--json') ? 'json' : 'summary'

class Table {
  map = new Map()
  get(key) { return this.map.get(key) }
  entries() { return this.map.entries() }
  get size() { return this.map.size }
  async put(key, value) { this.map.set(key, value) }
}

function parseCsv(text) {
  const [header, ...lines] = text.trim().split(/\r?\n/)
  const columns = header.split(',')
  return lines.filter((line) => line.trim()).map((line) => Object.fromEntries(
    line.split(',').map((value, index) => [columns[index], value]),
  ))
}

async function run() {
  const descriptions = parseCsv(await readFile(path.join(inputDir, 'descriptions.csv'), 'utf8'))
    .map((row) => row.description)
  const codes = parseCsv(await readFile(path.join(inputDir, 'codes.csv'), 'utf8')).map((row) => row.code)
  const elements = JSON.parse(await readFile(path.join(inputDir, 'elements.json'), 'utf8'))
  const rvcInput = JSON.parse(await readFile(path.join(inputDir, 'rvc.json'), 'utf8'))

  const tools = createTools({ classifications: new Table() })
  const byName = Object.fromEntries(tools.map((tool) => [tool.name, tool]))
  const call = { callId: 'quickstart' }

  const classifications = []
  for (const description of descriptions) {
    const classified = await byName['hs.classify'].execute({ description }, call)
    classifications.push({ description, top3: classified.top3.map((candidate) => candidate.code) })
  }
  const completeElements = await byName['hs.elements'].execute({ elements }, call)
  const emptyElements = await byName['hs.elements'].execute({ elements: {} }, call)
  const tariff = await byName['hs.tariff_version'].execute({}, call)
  const codeChecks = []
  for (const code of codes) {
    const checked = await byName['hs.code_check'].execute({ code }, call)
    codeChecks.push({ code, valid: checked.valid, ...(checked.reason ? { reason: checked.reason } : {}) })
  }
  const rvc = await byName['hs.rvc_report'].execute(rvcInput, call)

  return {
    sample: 'samples/quickstart/input/descriptions.csv',
    descriptions: descriptions.length,
    classifications,
    elements: {
      complete: completeElements.complete,
      missing_when_complete: completeElements.missing.length,
      missing_when_omitted: emptyElements.missing.length,
    },
    tariff_version: tariff.version,
    code_checks: codeChecks,
    rvc: {
      threshold_pct: rvc.threshold_pct,
      meets_threshold: rvc.meets_threshold,
      methods: rvc.methods,
    },
  }
}

const result = await run()

if (mode === 'json') {
  process.stdout.write(`${JSON.stringify(result, null, 2)}\n`)
} else if (mode === 'check') {
  const expected = JSON.parse(await readFile(expectedPath, 'utf8'))
  assert.deepEqual(result, expected)
  const rejected = result.code_checks.filter((entry) => !entry.valid)
  console.log('dsh-hs-candidate quickstart - synthetic products (not a real declaration)')
  console.log(`${result.descriptions} descriptions -> top3 candidates each`)
  console.log(`12-element check: complete=${result.elements.complete}, omitted fields=${result.elements.missing_when_omitted}`)
  console.log(`tariff version ${result.tariff_version}`)
  console.log(`code checks: ${result.code_checks.length - rejected.length} valid / ${rejected.length} rejected (${rejected.map((entry) => entry.reason).join(', ')})`)
  console.log(`RVC: ${result.rvc.methods.map((entry) => `${entry.method} ${entry.rvc_pct}`).join(', ')}; meets ${result.rvc.threshold_pct}% = ${result.rvc.meets_threshold}`)
  console.log('golden samples/quickstart/expected/result.json matches')
  console.log('quickstart ok')
} else {
  console.log('dsh-hs-candidate quickstart - synthetic products (not a real declaration)')
  console.log(`${result.descriptions} descriptions -> top3 candidates each`)
  console.log(`12-element check: complete=${result.elements.complete}, omitted fields=${result.elements.missing_when_omitted}`)
  console.log(`tariff version ${result.tariff_version}`)
  console.log(`code checks: ${result.code_checks.filter((entry) => entry.valid).length} valid / ${result.code_checks.filter((entry) => !entry.valid).length} rejected`)
  console.log(`RVC: ${result.rvc.methods.map((entry) => `${entry.method} ${entry.rvc_pct}`).join(', ')}; meets ${result.rvc.threshold_pct}% = ${result.rvc.meets_threshold}`)
  console.log('run with --check to compare against expected/result.json')
}
