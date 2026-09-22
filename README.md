# Heritage Protection Solutions — Landing Page

## Deploy on GitHub Pages

1. Create a new GitHub repository, e.g. `heritage-website`.
2. Upload **all files and folders from this ZIP to the repository root**.
   `index.html` must be visible at the top level.
3. Commit the files.
4. Go to **Settings → Pages**.
5. Under **Build and deployment**:
   - Source: `Deploy from a branch`
   - Branch: `main`
   - Folder: `/ (root)`
6. Save.
7. GitHub will provide a Pages URL such as:
   `https://YOUR-USERNAME.github.io/heritage-website/`

Keep the Wix production domain unchanged while reviewing this version.

## Later: custom domain
Once the site is approved, GitHub Pages can use a custom domain. Do not change the
Heritage DNS until the new site and any pages you need to preserve are ready.

## Main files
- `index.html` — landing page
- `assets/` — site imagery
- `.nojekyll` — disables Jekyll processing
- `404.html` — basic fallback page
