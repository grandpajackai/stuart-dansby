import asyncio,json,urllib.request
from playwright.async_api import async_playwright
B='http://localhost:8765/v2/'
PAGES={'corporate':'','education':'education/','course':'course/'}
async def main():
  async with async_playwright() as pw:
    br=await pw.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox'])
    issues=[]
    for name,path in PAGES.items():
      for wd in (1440,390,320):
        ctx=await br.new_context(viewport={'width':wd,'height':900},device_scale_factor=1)
        pg=await ctx.new_page(); errs=[]
        pg.on('console',lambda m,errs=errs: m.type in('error','warning') and errs.append(m.text))
        pg.on('pageerror',lambda e,errs=errs: errs.append(str(e)))
        pg.on('requestfailed',lambda r,errs=errs: errs.append('FAIL '+r.url))
        pg.on('response',lambda r,errs=errs: r.status>=400 and errs.append(f'{r.status} {r.url}'))
        await pg.goto(B+path,wait_until='networkidle')
        await pg.evaluate("document.querySelectorAll('.rv').forEach(e=>e.classList.add('in'))")
        await pg.evaluate("document.querySelectorAll('img[loading=lazy]').forEach(i=>i.loading='eager')")
        await pg.evaluate("(async()=>{for(let y=0;y<document.body.scrollHeight;y+=700){scrollTo(0,y);await new Promise(r=>setTimeout(r,60))}scrollTo(0,0)})()")
        await pg.wait_for_timeout(2500); await pg.wait_for_function("[...document.images].every(i=>i.complete&&i.naturalWidth)",timeout=15000)
        ov=await pg.evaluate("[document.documentElement.scrollWidth, innerWidth, [...document.querySelectorAll('body *')].filter(e=>{const r=e.getBoundingClientRect();return r.right>innerWidth+1 && getComputedStyle(e).position!='fixed' && !e.closest('.marquee')}).slice(0,5).map(e=>e.tagName+'.'+e.className)]")
        if ov[0]>ov[1] or ov[2]: issues.append(f'{name}@{wd} overflow {ov}')
        await pg.screenshot(path=f'/workspace/stuart/shots/{name}-{wd}.png',full_page=True)
        if errs: issues.append(f'{name}@{wd} console/net: {errs}')
        if wd==1440:
          info=await pg.evaluate("""({h1:document.querySelectorAll('h1').length,noalt:[...document.images].filter(i=>!i.hasAttribute('alt')).length,
          links:[...document.querySelectorAll('a[href]')].map(a=>a.getAttribute('href')),ids:[...document.querySelectorAll('[id]')].map(e=>e.id),
          smallTap:[...document.querySelectorAll('a,button')].filter(e=>{const r=e.getBoundingClientRect();return r.width&&r.height<24}).map(e=>e.textContent.trim().slice(0,30))})""")
          if info['h1']!=1 or info['noalt']: issues.append(f'{name} h1/alt {info["h1"]} {info["noalt"]}')
          for h in set(info['links']):
            if h.startswith('#'):
              if h[1:] not in info['ids']: issues.append(f'{name} bad anchor {h}')
            elif h.startswith(('mailto:','https://www.youtube')): pass
            else:
              u=urllib.parse.urljoin(B+path,h)
              try:
                if u.startswith('http://localhost'): urllib.request.urlopen(u.split('#')[0])
              except Exception as e: issues.append(f'{name} broken {h} {e}')
          # video dialog
          if name=='course': op,cl='x',True
          else:
           await pg.click('.hero [data-video]'); await pg.wait_for_timeout(500)
           op=await pg.evaluate("document.getElementById('video').open && !!document.querySelector('#video iframe') && document.activeElement.className")
           await pg.keyboard.press('Escape'); await pg.wait_for_timeout(200)
           cl=await pg.evaluate("!document.getElementById('video').open && !document.querySelector('#video iframe') && document.activeElement.hasAttribute('data-video')")
          if op!='x' or not cl: issues.append(f'{name} dialog {op} {cl}')
          # form invalid
          await pg.click('form [type=submit]')
          st=await pg.evaluate("[document.querySelector('.form-status').textContent, document.activeElement.id, document.querySelectorAll('[aria-invalid=true]').length]")
          if 'fix' not in st[0]: issues.append(f'{name} form invalid {st}')
          # fill valid, capture mailto
          for el in await pg.query_selector_all('form [required]'):
            tag=await el.evaluate('e=>e.tagName')
            if tag=='SELECT': await el.select_option(index=1)
            else: await el.fill('brandon@example.com' if await el.get_attribute('type')=='email' else 'Test Value')
          reqs=[]; pg.on('request',lambda r: reqs.append(r.url))
          try: await pg.click('form [type=submit]',timeout=3000)
          except Exception as e: print('click',e)
          await pg.wait_for_timeout(500)
          st=await pg.evaluate("document.querySelector('.form-status')?document.querySelector('.form-status').textContent:''")
          print(name,'form status:',st[:70]); 'Opening' in st or issues.append(name+' form valid fail')
        if wd==390:
          await pg.evaluate('scrollTo(0,0)')
          await pg.click('.menu-btn'); await pg.wait_for_timeout(350)
          await pg.screenshot(path=f'/workspace/stuart/shots/{name}-390-menu.png')
          ex=await pg.get_attribute('.menu-btn','aria-expanded'); fo=await pg.evaluate('document.activeElement.textContent')
          await pg.keyboard.press('Escape')
          ex2=await pg.get_attribute('.menu-btn','aria-expanded')
          if ex!='true' or ex2!='false': issues.append(f'{name} menu {ex} {ex2} {fo}')
        await ctx.close()
    await br.close()
    print('ISSUES:'); [print(' -',i) for i in issues]
import urllib.parse
asyncio.run(main())
