# Release verification

The release includes two separate, connected landing pages: corporate speaking and the introductory Five Pillars seminar. It follows the client’s updated page direction, including business credibility before the fighting story, all six complete executive testimonials, the revised pillar order, and original photography.

## Completed checks

- Static release checks: no errors or warnings across five HTML documents, local assets and links, JavaScript, metadata, structured data, and approved content.
- Browser regression: 37 checks covering desktop (1440px) and mobile (390px and 320px), all passing.
- Navigation and keyboard operation, package preselection, required-field validation, safe editable inquiry drafts, copy fallback, video dialogs and teardown, and the local reflection planner checked.
- No horizontal page overflow, broken local images, JavaScript exceptions, missing local resources, or unexpected network writes in the browser suite.
- Automated axe accessibility checks using WCAG A/AA rules: no detected violations across speaking, seminar, and privacy pages at all three widths, plus the seminar inquiry dialog.
- Independent visual review prompted fixes to mobile headline wrapping, benefits-heading size, photo cropping, contrast, iPhone field sizing, and email-draft preview height.

## Operational boundaries

Preparing an inquiry does not send an email. Visitors review a draft and send it through their own email app, or copy it to their preferred email service. Actual email delivery was not exercised during QA.

The seminar date and hosted payment destination have not been supplied. Its planned $9.99 / 75-minute format is visible, and the live action requests an invitation. The page does not accept money or claim to reserve a seat. Full-course details remain forthcoming.

Video dialog behavior is tested deterministically with the external iframe isolated. The client’s approved speaker reel and a direct YouTube fallback are configured; third-party video playback remains subject to YouTube availability.

Automated accessibility checks and browser testing are evidence of the tested behavior, not a guarantee for every device or third-party service.
