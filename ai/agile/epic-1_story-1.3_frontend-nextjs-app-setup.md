# Story 1.3: Frontend (Next.js) Application Setup with `pnpm`

## Status: Done

## Story

- As a Frontend Developer Agent
- I want to set up the foundational Next.js application structure for the frontend using `pnpm`
- so that UI development, component creation, and API integration can proceed in an organized, type-safe, and efficient manner, aligning with the Mailchimp aesthetic.

## Acceptance Criteria (ACs)

1. A new Next.js (`~15.3.2`) application is initialized within the `frontend/` directory using `pnpm`.
2. The Next.js application is configured to use TypeScript (`~5.5.2`).
3. Tailwind CSS (`~3.5.1`) is integrated into the Next.js application for styling.
4. `shadcn/ui` is initialized in the project (components to be added on-demand in later stories, but CLI setup can be done).
5. Lucide Icons (`lucide-react`) (`~0.425.0`) is added as a dependency.
6. A basic homepage (e.g., `app/page.tsx` or `app/(dashboard)/page.tsx` as per `frontend-architecture.md`) is created displaying a simple message (e.g., "Mailchimp Trends Engine - Frontend Placeholder").
7. A `Dockerfile` is created in the `frontend/` directory to containerize the Next.js application for production builds.
8. The Docker image for the frontend application can be built successfully.
9. The containerized frontend application can be run locally (e.g., via Docker command or eventually via k3s from Story 1.4), and the basic homepage is accessible.
10. `pnpm` scripts are configured in `frontend/package.json` for common development tasks (`dev`, `build`, `start`, `lint`, `test`).
11. Initial linter (ESLint with Next.js/TypeScript plugins) and formatter (Prettier) configurations are added to `frontend/`, and the initial code passes linting and formatting checks.
12. A `pnpm-workspace.yaml` file is created in the root directory to define `frontend` and `backend` (placeholder for backend if not directly managed by pnpm) as workspaces, if this approach is beneficial for root-level scripting. (Alternatively, manage frontend independently with `pnpm` within its directory).
13. `frontend/.env.local.example` is created, documenting `NEXT_PUBLIC_API_URL`.

## Tasks / Subtasks

- [x] Task 1: Initialize Next.js Project with TypeScript and `pnpm` (AC: #1, #2)
  - [x] Navigate to the `frontend/` directory.
  - [x] Initialize Next.js project using `pnpm create next-app@latest . --typescript --eslint --tailwind --src-dir --app --import-alias "@/*"` (or adjust flags for current best practices for Next.js 15, ensuring App Router and TypeScript).
  - [x] Verify `package.json` uses `pnpm`.
- [x] Task 2: Integrate Tailwind CSS (AC: #3)
  - [x] Ensure Tailwind CSS is set up during Next.js initialization (usually handled by `create-next-app` flags).
  - [x] Verify `tailwind.config.ts` and `postcss.config.mjs` are present and correctly configured.
  - [x] Create `frontend/src/app/globals.css` with Tailwind directives (`@import "tailwindcss";`).
  - [x] Define Mailchimp color palette and `fontFamily` (Helvetica Neue) in `frontend/tailwind.config.ts` and `frontend/src/app/globals.css`.
- [x] Task 3: Initialize `shadcn/ui` and Add Lucide Icons (AC: #4, #5)
  - [x] Initialize `shadcn/ui` using its `pnpm` CLI command (`pnpm dlx shadcn@latest init`). Follow prompts for configuration.
  - [x] Add `lucide-react` as a dependency: `pnpm add lucide-react`.
- [x] Task 4: Create Basic Homepage (AC: #6)
  - [x] Ensure `frontend/src/app/layout.tsx` and `frontend/src/app/page.tsx` are created.
  - [x] Modify the page component to display a simple placeholder message.
  - [x] Apply basic Mailchimp page background style and font in the root layout via `globals.css`.
- [x] Task 5: Create Frontend Dockerfile (AC: #7)
  - [x] Create `frontend/Dockerfile`.
  - [x] Use a multi-stage build.
    - [x] Stage 1 (Builder): Use `node:22-alpine` as `builder`. Set `WORKDIR`. Copy `package.json`, `pnpm-lock.yaml`. Run `pnpm install --frozen-lockfile`. Copy the rest of the frontend source. Run `pnpm build`.
    - [x] Stage 2 (Runner): Use `node:22-alpine` as `runner`. Set `WORKDIR`. Copy built assets (`.next/standalone`, `.next/static`, `public`) from the `builder` stage. Expose port 3000. Set `CMD ["node", "server.js"]`.
  - [x] Ensure `output: 'standalone'` is configured in `next.config.ts` for optimized Docker image.
- [x] Task 6: Configure Linters & Formatters (AC: #11)
  - [x] Ensure ESLint and Prettier are configured.
  - [x] Add Prettier config file (`frontend/.prettierrc.json`).
  - [x] ESLint config `frontend/eslint.config.mjs` was created by `create-next-app`.
  - [x] Ensure initial code passes linting (`pnpm lint --fix`) and formatting (`pnpm format`). (Installed `prettier` and `eslint-plugin-react-hooks`, `@next/eslint-plugin-next` to fix build issues).
- [x] Task 7: Define `pnpm` Scripts (AC: #10)
  - [x] Verify/update `frontend/package.json` scripts:
    - `dev`: `next dev` (removed `--turbopack`)
    - `build`: `next build`
    - `start`: `next start`
    - `lint`: `next lint`
    - `format`: `prettier --write "**/*.{ts,tsx,css,md,json}" --ignore-path .gitignore` (added)
    - `test`: (Placeholder for Jest setup in Story 1.6, e.g., `jest --watch`)
- [x] Task 8: Setup `pnpm` Workspaces (Optional but Recommended) (AC: #12)
  - [x] In the project root (outside `frontend/`), create `pnpm-workspace.yaml`.
  - [x] Add `packages:\n  - 'frontend'`
- [x] Task 9: Create `.env.local.example` (AC: #13)
  - [x] Create `frontend/.env.local.example` with `NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1`.
- [x] Task 10: Verify Docker Build and Run (AC: #8, #9)
  - [x] Build the Docker image.
  - [x] Run the container locally, mapping port 3000.
  - [x] Access the application in a browser to verify the basic homepage.

## Dev Technical Guidance

- **Next.js Initialization:** Use the latest stable version of `create-next-app` (`~15.3.2` specified). Prioritize App Router, TypeScript, Tailwind CSS integration during setup. `src/` directory is preferred.
- **`shadcn/ui` Initialization:** Follow the official `shadcn/ui` documentation for initialization. It will ask about `tailwind.config.js`, `globals.css`, CSS variables, etc. Accept defaults or configure as per project needs. No components need to be *added* in this story, just initialization.
- **Dockerfile Optimization:** Ensure the Dockerfile uses multi-stage builds to keep the final image small. `output: 'standalone'` in `next.config.mjs` is crucial for this.
- **Tailwind Theme:** Refer to `ui-ux-spec.md` and `Final-Mailchimp-Aligned-Dashboard-Mockup.png` for Mailchimp color palette (Cavendish Yellow, Peppercorn, Light Grey BG, etc.) and font (Helvetica Neue) to be added to `tailwind.config.js`.
- **Workspace Setup:** If using `pnpm` workspaces, ensure the `pnpm-workspace.yaml` is correctly configured at the project root. This can simplify running scripts across packages later.
- **Linters:** Standard Next.js ESLint setup is good. Integrate Prettier for consistent formatting.

## Story Progress Notes

### Completion Notes List

- Story completed successfully.
- Initial Docker build failed due to missing ESLint plugins (`eslint-plugin-react-hooks`, `@next/eslint-plugin-next`). These were installed, and the build then succeeded.
- `shadcn-ui` CLI package name was updated from `shadcn-ui` to `shadcn` during initialization.
- Tailwind CSS v4 setup by `create-next-app` uses `@import "tailwindcss";` and `@theme` directive in `globals.css`, which differs slightly from older Tailwind setups but is the current standard. Mailchimp theme colors and fonts were integrated into this new structure.
- Removed `--turbopack` from the `dev` script in `package.json` as it was not an intentional choice for this story.

### Change Log

- 2025-05-17 - Kayvan Sylvan - Initial draft
- 2025-05-19 - Cline - Completed all tasks and updated status to Done.
