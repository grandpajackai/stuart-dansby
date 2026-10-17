/* Independent browser QA. Uses synthetic details and never sends email or submits externally. */
const fs = require('node:fs');
const path = require('node:path');
const { chromium } = require(process.env.PLAYWRIGHT_MODULE || 'playwright');
const base = (process.env.QA_BASE || 'http://127.0.0.1:8768/stuart-dansby/').replace(/\/?$/, '/');
const output = path.resolve(process.env.QA_OUTPUT || path.join(__dirname, '../qa-artifacts'));
const results = [];
const issues = [];
const assert = (value, message) => { if (!value) throw new Error(message); };
async function check(name, fn) {
  try { const detail = await fn(); results.push({ name, passed: true, detail: detail || '' }); console.log('PASS', name); }
  catch (error) { results.push({ name, passed: false, detail: error.message }); issues.push(`${name}: ${error.message}`); console.log('FAIL', name, error.message); }
}
async function visibleDialog(page) { return page.locator('dialog[open]').first(); }
async function closeDialog(page) {
  const dialog = await visibleDialog(page);
  await dialog.locator('button').filter({ hasText: /close|×/i }).first().click();
}
async function main() {
  fs.mkdirSync(output, { recursive: true });
  fs.mkdirSync(path.join(output, 'qa'), { recursive: true });
  const browser = await chromium.launch({ executablePath: process.env.CHROME_EXECUTABLE || undefined, headless: true });
  for (const viewport of [{ width: 1440, height: 900 }, { width: 390, height: 844 }, { width: 320, height: 844 }]) {
    const context = await browser.newContext({ viewport, reducedMotion: 'reduce' });
    const page = await context.newPage();
    const runtimeErrors = [], failedLocal = [], externalRequests = [], writes = [];
    page.on('pageerror', error => runtimeErrors.push(error.message));
    page.on('response', response => { if (response.url().startsWith(base) && response.status() >= 400) failedLocal.push(`${response.status()} ${response.url()}`); });
    page.on('requestfailed', request => { if (request.url().startsWith(base)) failedLocal.push(`${request.failure()?.errorText} ${request.url()}`); });
    page.on('request', request => { if (request.method() !== 'GET') writes.push(`${request.method()} ${request.url()}`); });
    await page.route('**/*', route => {
      const url = route.request().url();
      if (/^https?:/.test(url) && !url.startsWith(base)) {
        externalRequests.push(url);
        return route.fulfill({ status: 200, contentType: 'text/html', body: '<!doctype html><html><title>Third-party embed isolated for UI QA</title></html>' });
      }
      return route.continue();
    });
    for (const route of ['speaking/', 'workshop/']) {
      const label = `${route} @ ${viewport.width}`;
      await check(`${label} load, assets, semantics and responsive layout`, async () => {
        const response = await page.goto(base + route, { waitUntil: 'networkidle' });
        assert(response && response.status() === 200, 'Page did not return 200');
        assert(await page.locator('h1').count() === 1, 'Expected exactly one h1');
        await page.evaluate(async () => { await document.fonts.ready; for (let y = 0; y < document.body.scrollHeight; y += 600) { window.scrollTo(0, y); await new Promise(resolve => setTimeout(resolve, 20)); } });
        await page.waitForLoadState('networkidle');
        const brokenImages = await page.locator('img').evaluateAll(images => images.filter(img => !img.complete || img.naturalWidth === 0).map(img => img.src));
        assert(!brokenImages.length, `Broken images: ${brokenImages.join(', ')}`);
        const dimensions = await page.evaluate(() => ({ viewport: innerWidth, html: document.documentElement.scrollWidth, body: document.body.scrollWidth }));
        assert(dimensions.html <= viewport.width + 1 && dimensions.body <= viewport.width + 1, `Horizontal overflow: ${JSON.stringify(dimensions)}`);
        const unlabelled = await page.locator('input:not([type=hidden]),textarea,select').evaluateAll(inputs => inputs.filter(input => !input.labels?.length && !input.getAttribute('aria-label') && !input.getAttribute('aria-labelledby')).map(input => input.id || input.name));
        assert(!unlabelled.length, `Unlabelled inputs: ${unlabelled.join(', ')}`);
        await page.evaluate(() => window.scrollTo(0, 0));
        await page.screenshot({ path: path.join(output, 'qa', `${route.replace('/', '')}-${viewport.width}-full.png`), fullPage: true });
        await page.screenshot({ path: path.join(output, 'qa', `${route.replace('/', '')}-${viewport.width}-viewport.png`) });
        return 'All local resources loaded; images decoded, fonts ready, one h1, labelled controls, no horizontal overflow.';
      });
      if (viewport.width < 761) {
        await check(`${label} mobile navigation keyboard and close`, async () => {
          const toggle = page.locator('[data-menu-toggle]');
          const nav = page.locator('#main-nav');
          await toggle.focus(); await page.keyboard.press('Enter');
          assert(await toggle.getAttribute('aria-expanded') === 'true' && await nav.isVisible(), 'Keyboard did not open menu');
          await page.keyboard.press('Escape');
          assert(await toggle.getAttribute('aria-expanded') === 'false', 'Escape did not close menu');
          await toggle.click(); await nav.locator('a').first().click();
          assert(await toggle.getAttribute('aria-expanded') === 'false', 'Anchor click did not close menu');
        });
      }
      await check(`${label} native form validation and review`, async () => {
        const form = page.locator(`form[data-inquiry="${route.replace('/', '')}"]`);
        await form.locator('button[type=submit]').click();
        assert(await page.locator('dialog[open]').count() === 0, 'Invalid form opened a review dialog');
        await form.locator('[name=name]').fill('QA Example <review>');
        await form.locator('[name=email]').fill('qa@example.invalid');
        if (route === 'speaking/') {
          await form.locator('[name=organization]').fill('QA Test Organization');
          await page.locator('[data-package]').nth(1).click();
          assert(await form.locator('[name=package]').inputValue() === 'Keynote + Breakout — $7,500', 'Package CTA did not preselect matching experience');
          await form.locator('[name=goals]').fill('Synthetic QA details only.\nSecond line & more.');
        } else await form.locator('[name=challenge]').fill('Synthetic QA interest; do not send.');
        await form.locator('button[type=submit]').click();
        const dialog = await visibleDialog(page);
        await dialog.waitFor({ state: 'visible' });
        const preview = dialog.locator('textarea');
        const text = await preview.inputValue();
        assert(text.includes('QA Example <review>') && text.includes('qa@example.invalid'), 'Draft omitted synthetic identity');
        assert(await dialog.locator('review').count() === 0, 'User text was interpreted as HTML');
        const email = dialog.locator('a[href^="mailto:"]');
        assert(await email.count() === 1, 'Expected one explicit email-app action');
        assert((await email.getAttribute('href')).startsWith('mailto:info@takingthefight.com'), 'Incorrect email destination');
        assert((await dialog.innerText()).match(/not|until|send/i), 'Review lacks delivery explanation');
        await page.keyboard.press('Escape');
        assert(await page.locator('dialog[open]').count() === 0, 'Escape did not close review dialog');
        return 'Validation blocks blank fields; package selection and safe text draft work. Email action inspected without opening it.';
      });
      await check(`${label} video dialog and teardown`, async () => {
        const opener = page.locator('[data-video]').first();
        await opener.click();
        const dialog = await visibleDialog(page); await dialog.waitFor({ state: 'visible' });
        const iframe = dialog.locator('iframe');
        assert(await iframe.count() === 1, 'Video iframe missing');
        assert((await iframe.getAttribute('src')).includes('5sc7bOOXswY'), 'Wrong video');
        assert(await iframe.getAttribute('title'), 'Video iframe missing title');
        const fallback = dialog.locator('a[href*="youtube"]');
        assert(await fallback.count() === 1, 'Video fallback link missing');
        await page.keyboard.press('Escape');
        assert(await page.locator('dialog[open]').count() === 0, 'Video does not close on Escape');
        await page.locator('dialog iframe[src*="5sc7bOOXswY"]').waitFor({ state: 'detached' });
        await page.waitForFunction(element => element === document.activeElement, await opener.elementHandle());
        return 'Correct titled iframe, fallback link, Escape close, playback removal and focus restoration. Third-party playback isolated.';
      });
      if (route === 'workshop/') await check(`${label} local reflection planner`, async () => {
        await page.locator('#w-planner-form button[type=submit]').click();
        assert(!await page.locator('#w-plan-result').isVisible(), 'Empty planner produces result');
        await page.locator('#w-challenge').fill('QA challenge <img src=x>');
        await page.locator('#w-action').fill('One small synthetic action.');
        await page.locator('#w-when').fill('Tomorrow before work.');
        await page.locator('#w-planner-form button[type=submit]').click();
        assert(await page.locator('#w-plan-result').isVisible(), 'Planner did not show result');
        assert((await page.locator('#w-output-challenge').innerText()).includes('<img src=x>'), 'Planner text escaped incorrectly');
        assert(await page.locator('#w-plan-result img').count() === 0, 'Planner interprets HTML');
        assert(await page.locator('#w-plan-result').evaluate(element => element === document.activeElement), 'Planner did not focus result');
        assert(await page.locator('#w-print-plan').isVisible(), 'Print/save option missing');
      });
      await check(`${label} accordion keyboard operation`, async () => {
        const details = page.locator('details').last();
        await details.locator('summary').focus(); await page.keyboard.press('Enter');
        assert(await details.getAttribute('open') !== null, 'Enter does not expand details');
        await page.keyboard.press('Enter');
        assert(await details.getAttribute('open') === null, 'Enter does not collapse details');
      });
    }
    await check(`Privacy @ ${viewport.width}`, async () => {
      const response = await page.goto(base + 'privacy/', { waitUntil: 'networkidle' });
      assert(response.status() === 200 && await page.locator('h1').count() === 1, 'Privacy page missing');
      assert((await page.locator('body').innerText()).match(/email/i), 'Privacy does not explain email handling');
      assert(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth + 1), 'Privacy overflows horizontally');
    });
    await check(`Runtime/resource/external-write audit @ ${viewport.width}`, async () => {
      assert(!runtimeErrors.length, `JS exceptions: ${runtimeErrors.join('; ')}`);
      assert(!failedLocal.length, `Local resource failures: ${failedLocal.join('; ')}`);
      assert(!writes.length, `Unexpected network writes: ${writes.join('; ')}`);
      return `Zero JS exceptions, zero local resource failures, zero network writes. ${externalRequests.length} public video requests isolated.`;
    });
    await context.close();
  }
  const copyContext = await browser.newContext({ viewport: { width: 1440, height: 900 }, reducedMotion: 'reduce' });
  const copyPage = await copyContext.newPage();
  await copyPage.addInitScript(() => { Object.defineProperty(navigator, 'clipboard', { configurable: true, value: { writeText: () => Promise.reject(new Error('Clipboard deliberately unavailable in QA')) } }); });
  await check('Clipboard-unavailable manual copy fallback', async () => {
    await copyPage.goto(base + 'workshop/', { waitUntil: 'networkidle' });
    const form = copyPage.locator('[data-inquiry="workshop"]');
    await form.locator('[name=name]').fill('QA Copy'); await form.locator('[name=email]').fill('qa@example.invalid');
    await form.locator('button[type=submit]').click();
    const dialog = await visibleDialog(copyPage); await dialog.waitFor({ state: 'visible' });
    await dialog.locator('button').filter({ hasText: /copy/i }).click();
    assert((await dialog.innerText()).match(/select|selected|copy/i), 'No manual copy guidance');
    const selection = await dialog.locator('textarea').evaluate(element => ({ start: element.selectionStart, end: element.selectionEnd, length: element.value.length }));
    assert(selection.start === 0 && selection.end === selection.length && selection.length > 0, 'Draft not selected for manual copy');
  });
  await copyContext.close(); await browser.close();
  const report = `# Independent functional QA\n\nBase: ${base}\nGenerated: ${new Date().toISOString()}\n\n${results.filter(result => result.passed).length}/${results.length} checks passed.\n\n${results.map(result => `- ${result.passed ? 'PASS' : 'FAIL'} — ${result.name}${result.detail ? `: ${result.detail}` : ''}`).join('\n')}\n\n## Scope and limits\n\nTests use synthetic data only and never open email actions or submit data externally. Video dialog behavior is tested with a synthetic third-party iframe response; real YouTube delivery/playback is outside this deterministic browser suite. Screenshots at 1440, 390 and 320 pixels saved alongside this report.\n`;
  fs.writeFileSync(path.join(output, 'functional-qa.md'), report);
  if (issues.length) process.exitCode = 1;
}
main().catch(error => { fs.mkdirSync(output, { recursive: true }); fs.writeFileSync(path.join(output, 'functional-qa.md'), `# QA blocked\n\n${error.stack}\n`); console.error(error); process.exitCode = 1; });
