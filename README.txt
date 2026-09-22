HERITAGE LANDING V4 — CACHE-BUSTED WIX/GITHUB DEPLOYMENT

FIRST: RESTORE THE LIVE SITE
1. In Wix Pages, set your previous working page (Clarity Consult / old Home) back as Home.
2. Publish.
3. Open the public site in an incognito/private window and confirm it loads.

DO NOT DELETE the new Landing Page.

THEN TEST V4 SAFELY
1. Upload heritage-landing-v4.js to the ROOT of the GitHub repo:
   metahero350-byte/Heritageprosolutions

2. Confirm GitHub Pages serves:
   https://metahero350-byte.github.io/Heritageprosolutions/heritage-landing-v4.js

3. On the hidden/new Landing Page in Wix, select the Custom Element.

4. Choose Source > Server URL:
   https://metahero350-byte.github.io/Heritageprosolutions/heritage-landing-v4.js

5. Change tag name to:
   heritage-landing-v4

6. Save.

7. Test ONLY the hidden Landing Page first.
   Hard refresh with Ctrl+Shift+R or use an incognito/private window.

8. Confirm:
   - Full landing page loads
   - New wealth-category placement appears before Blueprint
   - Explore modals work
   - 8 Wealth Building guide opens correctly
   - Calendly links work
   - Desktop/mobile layout looks right

9. ONLY AFTER THAT:
   Set the new Landing Page as Home and publish again.

WHY V4
The new filename and custom-element tag avoid stale GitHub Pages/browser/Wix caching
and avoid reusing an already-registered custom element name.
