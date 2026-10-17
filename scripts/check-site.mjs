#!/usr/bin/env node
/** Static release checks. Run from any directory with `node scripts/check-site.mjs`.
 * This verifies source integrity; it does not claim browser or delivery verification.
 */
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { spawnSync } from 'node:child_process';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const errors = [];
const warnings = [];
const fail = (file, message) => errors.push(`${path.relative(root, file) || '.'}: ${message}`);
const warn = (file, message) => warnings.push(`${path.relative(root, file) || '.'}: ${message}`);
function walk(dir) {
  return fs.readdirSync(dir, { withFileTypes: true }).flatMap(entry => {
    if (['.git', 'node_modules', '.DS_Store', 'test-results', 'playwright-report'].includes(entry.name)) return [];
    const target = path.join(dir, entry.name);
    return entry.isDirectory() ? walk(target) : [target];
  });
}
const files = walk(root);
const pages = files.filter(file => file.endsWith('.html'));
const sourceText = new Map(pages.map(file => [file, fs.readFileSync(file, 'utf8')]));
const projectName = [...sourceText.values()].map(html => html.match(/https:\/\/[^/]+\.github\.io\/([^/]+)\//)?.[1]).find(Boolean);
const projectPrefix = projectName ? `/${projectName}/` : null;
function decode(text) {
  return text.replace(/&(?:amp|#38);/g, '&').replace(/&(?:quot|#34);/g, '"')
    .replace(/&(?:apos|#39|#x27);/g, "'").replace(/&(?:nbsp|#160);/g, ' ')
    .replace(/&#(\d+);/g, (_, n) => String.fromCodePoint(Number(n)))
    .replace(/&#x([\da-f]+);/gi, (_, n) => String.fromCodePoint(parseInt(n, 16)));
}
function normal(text) {
  return decode(text.replace(/<[^>]*>/g, ' ')).replace(/[‘’]/g, "'")
    .replace(/[“”]/g, '"').replace(/[–—]/g, '-').replace(/\s+/g, ' ').trim();
}
function attrs(tag) {
  return Object.fromEntries([...tag.matchAll(/([\w:-]+)\s*=\s*(?:"([^"]*)"|'([^']*)'|([^\s>]+))/g)]
    .map(m => [m[1].toLowerCase(), decode(m[2] ?? m[3] ?? m[4])]));
}
const allIds = new Map(pages.map(file => [file, new Set([...sourceText.get(file).matchAll(/\bid\s*=\s*["']([^"']+)["']/g)].map(m => m[1]))]));

function checkReference(file, value, kind) {
  if (!value || /^(?:mailto:|tel:|data:|blob:|https?:|\/\/)/i.test(value)) return;
  if (/^(?:javascript:|file:)/i.test(value)) return fail(file, `Unsafe ${kind}: ${value}`);
  const [withoutHash, fragment] = value.split('#');
  let pathname = withoutHash.split('?')[0];
  let base = path.dirname(file);
  if (value.startsWith('/')) {
    if (!projectPrefix || !pathname.startsWith(projectPrefix)) return fail(file, `Root-relative ${kind} is outside the GitHub Pages project: ${value}`);
    pathname = pathname.slice(projectPrefix.length);
    base = root;
  }
  let target;
  try { target = pathname ? path.resolve(base, decodeURIComponent(pathname)) : (value.startsWith('/') ? root : file); }
  catch { return fail(file, `Malformed ${kind}: ${value}`); }
  if (!target.startsWith(`${root}${path.sep}`) && target !== root) return fail(file, `${kind} escapes the site: ${value}`);
  if (fs.existsSync(target) && fs.statSync(target).isDirectory()) target = path.join(target, 'index.html');
  if (!fs.existsSync(target)) return fail(file, `Missing ${kind} target: ${value}`);
  if (fragment && target.endsWith('.html')) {
    let id;
    try { id = decodeURIComponent(fragment); } catch { return fail(file, `Malformed fragment: ${value}`); }
    if (!allIds.get(target)?.has(id)) fail(file, `Missing anchor: ${value}`);
  }
}

if (!pages.length) fail(root, 'No HTML pages exist.');
for (const expected of ['index.html', 'speaking/index.html', 'workshop/index.html', 'privacy/index.html']) {
  if (!fs.existsSync(path.join(root, expected))) fail(root, `Required page missing: ${expected}`);
}
for (const [file, html] of sourceText) {
  if (!/<!doctype html>/i.test(html)) fail(file, 'Missing HTML doctype.');
  if (!/<html\b[^>]*\blang=["']en["']/i.test(html)) fail(file, 'Missing English document language.');
  if (!/<meta\b[^>]*\bname=["']viewport["']/i.test(html)) fail(file, 'Missing mobile viewport.');
  const title = html.match(/<title>([^<]+)<\/title>/i)?.[1];
  if (!title?.trim()) fail(file, 'Missing document title.');
  if ((html.match(/<h1\b/gi) || []).length !== 1) fail(file, 'Expected exactly one H1.');
  if (!/<meta\b[^>]*\bname=["']description["'][^>]*\bcontent=["'][^"']+/i.test(html)) fail(file, 'Missing description.');
  const ids = [...html.matchAll(/\bid\s*=\s*["']([^"']+)["']/g)].map(m => m[1]);
  if (new Set(ids).size !== ids.length) fail(file, 'Duplicate element IDs.');
  const canonicals = [...html.matchAll(/<link\b[^>]*>/gi)].map(m => attrs(m[0])).filter(a => a.rel === 'canonical');
  const isPublic = !/<meta\b[^>]*name=["']robots["'][^>]*content=["'][^"']*noindex/i.test(html);
  if (canonicals.length !== 1 && isPublic) warn(file, 'Expected one canonical URL.');
  for (const a of canonicals) if (!/^https:\/\//.test(a.href || '') || /localhost|example\.(com|org)|PLACEHOLDER/i.test(a.href)) fail(file, 'Canonical is not a real HTTPS public URL.');
  if (isPublic && !/<meta\b[^>]*property=["']og:image["']/i.test(html)) warn(file, 'Missing social preview image.');
  for (const m of html.matchAll(/<(a|link|script|img|source|iframe|video)\b[^>]*>/gi)) {
    const a = attrs(m[0]);
    const tag = m[1].toLowerCase();
    if (tag === 'a' || tag === 'link') checkReference(file, a.href, `${tag} href`);
    else checkReference(file, a.src, `${tag} src`);
    if (a.poster) checkReference(file, a.poster, 'video poster');
    if (a.srcset) for (const candidate of a.srcset.split(',')) checkReference(file, candidate.trim().split(/\s+/)[0], 'srcset');
    if (tag === 'img' && !Object.hasOwn(a, 'alt')) fail(file, `Image has no alt attribute: ${a.src}`);
    if (tag === 'iframe' && !a.title) fail(file, 'Iframe is missing its accessible title.');
    if (a.target === '_blank' && !/noopener|noreferrer/.test(a.rel || '')) warn(file, `New-tab link is missing noopener: ${a.href}`);
    if (a.href === '#') fail(file, 'Placeholder anchor with no destination.');
  }
  for (const m of html.matchAll(/<script\b([^>]*)>([\s\S]*?)<\/script>/gi)) {
    const a = attrs(m[1]);
    if (a.type === 'application/ld+json') {
      try { JSON.parse(m[2]); } catch (e) { fail(file, `Invalid JSON-LD: ${e.message}`); }
    }
  }
  for (const m of html.matchAll(/<form\b([^>]*)>([\s\S]*?)<\/form>/gi)) {
    const a = attrs(m[1]);
    const namedFields = /<(?:input|textarea|select)\b[^>]*\bname\s*=/i.test(m[2]);
    if (namedFields && !a.action && (a.method || 'get').toLowerCase() !== 'dialog') {
      fail(file, 'Named form fields can leak into the URL when JavaScript is unavailable; specify a safe native fallback.');
    }
  }
  if (/\/Users\/|\/Downloads\/|client-feedback-extracted|source-audit|revenue-meeting-extracted/i.test(html)) fail(file, 'Private workspace/source reference appears in public HTML.');
  if (/Brandon Gil|profit share|September 9, 2026|revenue generation meeting/i.test(normal(html))) fail(file, 'Private planning data appears in public HTML.');
  if (/payment successful|order confirmed|seat confirmed|registration confirmed|you(?:'|’)re registered/i.test(normal(html))) warn(file, 'Check that confirmation wording reflects an actual completed action.');
}
for (const file of files.filter(file => file.endsWith('.css'))) {
  for (const m of fs.readFileSync(file, 'utf8').matchAll(/url\(\s*["']?([^"')]+)["']?\s*\)/g)) checkReference(file, m[1].trim(), 'CSS asset');
}
for (const file of files.filter(file => /\.(?:m?js)$/.test(file) && !file.includes(`${path.sep}scripts${path.sep}`))) {
  const result = spawnSync(process.execPath, ['--check', file], { encoding: 'utf8' });
  if (result.status !== 0) fail(file, `JavaScript syntax check failed: ${result.stderr.trim()}`);
}
for (const file of files) {
  if (/\.(docx?|zip|pem|key)$/i.test(file) || /(?:^|\/)(?:\.env|client-feedback|source-audit|revenue-meeting)/.test(file)) fail(file, 'Private document, archive, or credential file in site.');
}

const speakingFile = path.join(root, 'speaking/index.html');
const workshopFile = path.join(root, 'workshop/index.html');
const testimonials = [
  ['Jonathan Thompson', 'Chief Executive Officer, Nielsen-Massey Vanillas', "Stuart is a passionate and driven leader with tremendous EQ, commercial acumen, and organizational agility. He's an asset and a force multiplier."],
  ['David Stis', 'Chief Commercial Officer, Del Monte Foods', 'A visionary executive who builds high-performing business models, develops exceptional teams, and consistently delivers results with integrity and character.'],
  ['David Klavsons', 'Chief Executive Officer, King Juice', "One of the most passionate and motivating leaders I've ever met. Stuart consistently rallies organizations to deliver beyond expectations."],
  ['Sheila Rondeau', 'CEO, MOGXP', 'A strategic executive who combines vision, innovation, and disciplined execution while inspiring teams and driving measurable business growth.'],
  ['John Albert III', 'Chief Executive Officer, Unified Building Group', "Stuart saw strengths in me I didn't yet recognize. His mentorship shaped both my career and the leader I've become."],
  ['Saverio Spontella', 'Chief Commercial & Marketing Officer', 'A high-performing commercial leader whose passion, strategic thinking, and ability to build new capabilities consistently drive growth and innovation.'],
];
if (sourceText.has(speakingFile)) {
  const text = normal(sourceText.get(speakingFile));
  for (const [name, title, quote] of testimonials) {
    if (!text.includes(name)) fail(speakingFile, `Missing approved endorser: ${name}`);
    if (!text.includes(normal(title))) fail(speakingFile, `Missing exact supplied title for ${name}`);
    if (!text.includes(normal(quote))) fail(speakingFile, `Missing exact complete quote for ${name}`);
  }
}
const pillarNames = [
  'The Difference Between Stress and Challenge Is Perspective',
  'Everything Good in Life Comes From Discipline',
  'Your Real Competition Is You',
  'Servant Leadership and the Power of the Team',
  'Championship Performance',
];
for (const file of [speakingFile, workshopFile]) {
  if (!sourceText.has(file)) continue;
  const html = sourceText.get(file);
  const text = normal(html);
  if (!text.includes("The arena changes. The principles don't.")) fail(file, 'Missing approved brand anchor.');
  if (!text.includes('Stuart Warren Dansby')) fail(file, 'Missing full branded name.');
  let previous = -1;
  // Use headings to avoid an incidental mention of "championship performance" in introductory prose.
  const headings = [...html.matchAll(/<h[2-6]\b[^>]*>([\s\S]*?)<\/h[2-6]>/gi)].map(m => normal(m[1]));
  for (const name of pillarNames) {
    const index = headings.findIndex((heading, i) => i > previous && heading.toLowerCase().includes(name.toLowerCase()));
    if (index < 0) fail(file, `Missing full approved pillar heading or incorrect sequence: ${name}`);
    else previous = index;
  }
}
if (sourceText.has(workshopFile)) {
  const html = sourceText.get(workshopFile);
  const header = html.match(/<header\b[^>]*>([\s\S]*?)<\/header>/i)?.[1] || '';
  if (/\$9\.99|save my seat|reserve.*seat/i.test(normal(header))) fail(workshopFile, 'Seminar top navigation includes the registration/price CTA removed by client feedback.');
}

console.log(`Checked ${pages.length} HTML pages, ${files.length} site files, local URLs, CSS assets, JSON-LD, JavaScript syntax, privacy, and approved content.`);
for (const message of warnings) console.log(`WARN ${message}`);
for (const message of errors) console.error(`FAIL ${message}`);
console.log(`${errors.length} error(s), ${warnings.length} warning(s).`);
process.exitCode = errors.length ? 1 : 0;
