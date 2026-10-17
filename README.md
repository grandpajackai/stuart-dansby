# Taking the Fight · Stuart Warren Dansby

Two distinct visitor journeys built as fast, accessible static pages.

- [Speaking](https://grandpajackai.github.io/stuart-dansby/speaking/)
- [Introductory seminar](https://grandpajackai.github.io/stuart-dansby/workshop/)

The root URL opens the speaking experience. The seminar has its own landing page, navigation, narrative, and invitation flow. Secondary connections follow the client’s updated page direction.

## Run locally

Use any static HTTP server. To simulate the repository path, serve this directory under `/stuart-dansby/`.

Run `node scripts/check-site.mjs` to validate local links, assets, metadata, approved copy, and JavaScript syntax. GitHub Actions runs the same checks before every Pages deployment. No package installation or build step is needed.

## Inquiry behavior

Forms prepare editable email drafts addressed to `info@takingthefight.com`. The visitor must send the email in their own email app, or copy it to their preferred email service. Preparing a draft does not submit information, book an event, reserve a seat, or take payment. No backend, third-party form processor, or analytics has been added.

## Seminar launch

The $9.99 ticket and 75-minute live online format are planning details from the supplied prototype and latest page direction. A session date and live checkout have not been supplied. The page therefore requests an invitation instead of accepting payment. The full course is described as a future continuation without a dead link or purchase claim. Connect confirmed scheduling and a real hosted checkout before changing invitation buttons to paid registration.

## Sources and media

Copy follows the client’s updated page-layout document and supplied press kit. Original photos depict Stuart Warren Dansby and are reproduced from client assets and the official Taking the Fight site; his appearance has not been altered. Photography is optimized to WebP. Speaker video is the client-supplied YouTube reel `5sc7bOOXswY` and loads only after interaction. Barlow Condensed and DM Sans are open fonts from Google Fonts, licensed under the SIL Open Font License; license texts are in `assets/licenses/`.

## Custom domain handoff

Set the domain in repository **Settings → Pages → Custom domain**, then point the domain’s DNS to GitHub Pages following GitHub’s instructions. This repository deliberately has no `CNAME` yet. After switching the domain, update canonical URLs, Open Graph URLs, the Person JSON-LD URL, `robots.txt`, and `sitemap.xml` to the production domain. Root-relative recovery links in `404.html` should also be updated for a root-domain launch. Regular navigation and assets use relative paths.

## Browser QA

The optional browser suite uses Playwright and an installed Chromium browser, outside the production site. With Playwright available, run `node scripts/browser-qa.cjs`. Use `PLAYWRIGHT_MODULE` and `CHROME_EXECUTABLE` to select existing installations, `QA_BASE` to test a live deployment, and `QA_OUTPUT` to choose the report directory. Reports default to ignored `qa-artifacts/`. Tests use synthetic details, isolate third-party video responses, and never send an email. See [QA.md](QA.md) for release scope and operational boundaries.
