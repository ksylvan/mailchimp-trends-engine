# Story 1.3: Frontend (Next.js) Application Setup with `pnpm`

## Status: Draft

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

- [ ] Task 1: Initialize Next.js Project with TypeScript and `pnpm` (AC: #1, #2)
  - [ ] Navigate to the `frontend/` directory.
  - [ ] Initialize Next.js project using `pnpm create next-app@latest . --typescript --eslint --tailwind --src-dir --app --import-alias "@/*"` (or adjust flags for current best practices for Next.js 15, ensuring App Router and TypeScript).
  - [ ] Verify `package.json` uses `pnpm`.
- [ ] Task 2: Integrate Tailwind CSS (AC: #3)
  - [ ] Ensure Tailwind CSS is set up during Next.js initialization (usually handled by `create-next-app` flags).
  - [ ] Verify `tailwind.config.js` and `postcss.config.mjs` are present and correctly configured.
  - [ ] Create `frontend/app/globals.css` with Tailwind directives (`@tailwind base; @tailwind components; @tailwind utilities;`).
  - [ ] Define Mailchimp color palette and `fontFamily` (Helvetica Neue) in `frontend/tailwind.config.js` under `theme.extend` as per `frontend-architecture.md` and `ui-ux-spec.md`.
- [ ] Task 3: Initialize `shadcn/ui` and Add Lucide Icons (AC: #4, #5)
  - [ ] Initialize `shadcn/ui` using its `pnpm` CLI command (e.g., `pnpm dlx shadcn-ui@latest init`). Follow prompts for configuration (e.g., `globals.css` location, CSS variables, `tailwind.config.js`).
  - [ ] Add `lucide-react` as a dependency: `pnpm add lucide-react`.
- [ ] Task 4: Create Basic Homepage (AC: #6)
  - [ ] Ensure `frontend/app/layout.tsx` and `frontend/app/page.tsx` (or `frontend/app/(dashboard)/page.tsx` and `frontend/app/(dashboard)/layout.tsx` if using a route group immediately) are created.
  - [ ] Modify the page component to display a simple placeholder message.
  - [ ] Apply basic Mailchimp page background style (e.g., `bg-light-grey-bg` from `globals.css`/`tailwind.config.js`) in the root layout.
- [ ] Task 5: Create Frontend Dockerfile (AC: #7)
  - [ ] Create `frontend/Dockerfile`.
  - [ ] Use a multi-stage build.
    - [ ] Stage 1 (Builder): Use `node:22-alpine` (or similar Node.js 22 base) as `builder`. Set `WORKDIR`. Copy `package.json`, `pnpm-lock.yaml`. Run `pnpm install --frozen-lockfile`. Copy the rest of the frontend source. Run `pnpm build`.
    - [ ] Stage 2 (Runner): Use `node:22-alpine` as `runner`. Set `WORKDIR`. Copy built assets (`.next/standalone` or `.next` static and public folders) from the `builder` stage. Expose port 3000. Set `CMD ["node", "server.js"]` (or appropriate command for Next.js standalone output).
  - [ ] Ensure `output: 'standalone'` is configured in `next.config.mjs` for optimized Docker image.
- [ ] Task 6: Configure Linters & Formatters (AC: #11)
  - [ ] Ensure ESLint and Prettier are configured (typically done by `create-next-app` and can be customized).
  - [ ] Add Prettier config file (e.g., `.prettierrc.json`).
  - [ ] Add ESLint config file (e.g., `.eslintrc.json`).
  - [ ] Ensure initial code passes linting (`pnpm lint`) and formatting.
- [ ] Task 7: Define `pnpm` Scripts (AC: #10)
  - [ ] Verify/update `frontend/package.json` scripts:
    - `dev`: `next dev`
    - `build`: `next build`
    - `start`: `next start`
    - `lint`: `next lint`
    - `test`: (Placeholder for Jest setup in Story 1.6, e.g., `jest --watch`)
- [ ] Task 8: Setup `pnpm` Workspaces (Optional but Recommended) (AC: #12)
  - [ ] In the project root (outside `frontend/`), create `pnpm-workspace.yaml`.
  - [ ] Add `packages:\n  - 'frontend'\n  - 'backend'` (or just `frontend` if backend isn't managed by pnpm).
- [ ] Task 9: Create `.env.local.example` (AC: #13)
  - [ ] Create `frontend/.env.local.example` with `NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1`.
- [ ] Task 10: Verify Docker Build and Run (AC: #8, #9)
  - [ ] Build the Docker image.
  - [ ] Run the container locally, mapping port 3000.
  - [ ] Access the application in a browser to verify the basic homepage.

## Dev Technical Guidance

- **Next.js Initialization:** Use the latest stable version of `create-next-app` (`~15.3.2` specified). Prioritize App Router, TypeScript, Tailwind CSS integration during setup. `src/` directory is preferred.
- **`shadcn/ui` Initialization:** Follow the official `shadcn/ui` documentation for initialization. It will ask about `tailwind.config.js`, `globals.css`, CSS variables, etc. Accept defaults or configure as per project needs. No components need to be *added* in this story, just initialization.
- **Dockerfile Optimization:** Ensure the Dockerfile uses multi-stage builds to keep the final image small. `output: 'standalone'` in `next.config.mjs` is crucial for this.
- **Tailwind Theme:** Refer to `ui-ux-spec.md` and `Final-Mailchimp-Aligned-Dashboard-Mockup.png` for Mailchimp color palette (Cavendish Yellow, Peppercorn, Light Grey BG, etc.) and font (Helvetica Neue) to be added to `tailwind.config.js`.
- **Workspace Setup:** If using `pnpm` workspaces, ensure the `pnpm-workspace.yaml` is correctly configured at the project root. This can simplify running scripts across packages later.
- **Linters:** Standard Next.js ESLint setup is good. Integrate Prettier for consistent formatting.

## Story Progress Notes

### Completion Notes List

{Any notes about implementation choices, difficulties, or follow-up needed}

### Change Log

- 2025-05-17 - Kayvan Sylvan - Initial draft
