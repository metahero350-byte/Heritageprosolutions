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

## Blog
Posts live in `blog-src/` as Markdown files (one file per post, front matter at the top:
`title`, `slug`, `date`, optional `description`, `cover`). To publish a new post:

1. Add `blog-src/<slug>.md`.
2. Run `python3 tools/build_blog.py` (needs `pip install markdown`).
3. Commit everything. GitHub Pages publishes `post/<slug>/`, `blog/`, and `blog/posts.json`.

The homepage "From the Heritage Blog" section reads `blog/posts.json` and always shows the 3 newest posts.
Post URLs match the old Wix URLs (`/post/<slug>`), so links and search rankings carry over when the domain moves.
