# hofmannmoritz.com

One page: e-commerce portfolio (carousel) and the wedding website offer, German at `/`,
English at `/en/`. Static files on GitHub Pages, behind Cloudflare.

- Edit texts in `build.py`, then `python3 build.py` writes `index.html`, `en/index.html`,
  imprint and privacy policy (DE + EN). Commit the generated files too.
- The wedding section is `src/hochzeit-de.html` / `src/hochzeit-en.html`, the markup of
  fastpal.com/hochzeit from 2026-10-24, styled by `assets/hochzeit.css` (copied unchanged
  from fastpal-next `apps/web/app/hochzeit/hochzeit.css`).
- The wedding form posts to `https://fastpal.com/api/anfrage` (Resend mail to Moritz);
  that route allows this origin (CORS).
- Fonts are self-hosted in `assets/fonts` (no requests to Google). Mail addresses are only
  in the HTML as reversed base64 and filled in by `assets/site.js`.
- `id/` keeps the redirect for hofmannmoritz.id.
- Domains: Cloudflare workers, script `~/.claude/scripts/cloudflare/hofmannmoritz-redirect.py`.
