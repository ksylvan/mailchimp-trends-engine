# Mailchimp Marketing Trends Engine Product Requirements Document (PRD)

**Version:** 1.0
**Date:** May 16, 2025
**Project Owner:** User
**Author:** 2-pm (AI Product Manager)

## 1. Goal, Objective and Context

* **Overall Goal:** To design, build, and demonstrate a working prototype of a Marketing Trends Engine that scans the web for real-time marketing trends, providing actionable insights. A secondary goal is to showcase technical expertise through a comprehensive presentation of this system.
* **Primary Objective (Prototype):**
  * Develop a system capable of identifying and processing marketing trends from selected online news sources.
  * Provide a user-friendly dashboard for visualizing these trends, with a UI aligned with Mailchimp's aesthetics.
  * Generate actionable marketing content ideas (e.g., email subject lines, body copy) based on identified trends using an LLM (Anthropic Claude for MVP).
* **Primary Objective (Presentation):**
  * Deliver a 75-minute presentation detailing the system's design, functionality (with a live demo), and technical underpinnings.
  * Clearly articulate personal motivation, professional achievements, and how the project aligns with programming fundamentals, product engineering, AI implementation, and tech adaptability.
* **Context:** This project serves as a means to demonstrate advanced technical and product development skills in a challenging, time-constrained scenario (3-4 day development timeline). The focus is on creating an impressive and functional prototype that highlights capabilities in real-time data processing, AI/ML (NLP and LLM integration), system architecture (cloud-ready, containerized), and UI/UX. The prototype and presentation are key deliverables for an evaluation focusing on practical application and technical depth.
* **Target User (for the conceptual product):** The Mailchimp user, typically a business owner or their designated marketing department/personnel, who is looking for ways to enhance their marketing campaigns with timely and relevant trend data and content inspiration.

## 2. Functional Requirements (MVP)

The MVP of the Mailchimp Marketing Trends Engine will enable users to discover, analyze, and get AI-generated content ideas from marketing-relevant trends identified from news sources.

* **FR1: Trend Data Collection & Initial Content Extraction**

  * **FR1.1: Pluggable Data Source Architecture:** The system shall be designed with a modular/plugin architecture for data collection.
  * **FR1.2: Mock Data Source Plugin (MVP):** The system shall include a mock data plugin to generate or serve pre-defined datasets simulating marketing trends and associated text content for development and testing.
  * **FR1.3: News Content Extraction Plugin (MVP using Jina AI Reader):**
    * The system shall utilize Jina AI's Reader capability (e.g., via direct calls to the `https://r.jina.ai/` endpoint without an API key) to fetch and extract the primary textual content from a configurable list of 3-5 diverse general news websites.
    * This plugin will be scheduled to periodically fetch new articles.
    * The plugin shall output the full extracted Markdown or plain text content of each article.
  * **FR1.4: Raw Content Storage (Preliminary):** The system shall store fetched raw article text and basic metadata (source URL, timestamp) in a simple, accessible way for the MVP (e.g., uniquely named files on a Docker volume).
  * **FR1.5: Focused Secondary Search Capability (Design for MVP):** The system shall be designed to allow for secondary, focused searches (e.g., using Jina AI `s.reader` with an API key) based on initially identified topics to gather more marketing-specific context. Implementation of automated secondary search is post-MVP, but the design will be considered.

* **FR2: Trend Data Processing & Analysis (MVP Scope)**

  * **FR2.1: Raw Text Processing:** The system shall process the full textual content obtained from FR1.3 or FR1.2.
  * **FR2.2: NLP for Topic & Marketing Relevance:**
    * Perform NLP (cleaning, tokenization, stop-word removal, lemmatization) on the full text.
    * Extract topics/themes using a pre-trained transformer model (from Hugging Face).
    * Perform basic sentiment analysis (positive, negative, neutral) on topics/articles.
    * Assess "marketing relevance" of topics via keyword matching against a configurable marketing ontology.
  * **FR2.3: Trend Identification Algorithms:** Identify trends based on mention frequency and growth rate of *marketing-relevant* topics. Compute a trend score.
  * **FR2.4: Trend Categorization:** Categorize identified marketing trends based on marketing relevance assessment.

* **FR3: Trend Visualization & Dashboard (MVP Scope)**

  * Provide a user-friendly web dashboard (Next.js) to display identified marketing trends.
  * Allow users to view a list/cards of current trends with key info (name, date, sentiment, score).
  * Provide basic filtering (by category, sentiment).
  * Display time-series visualizations for selected trends (evolution of mention frequency/score).

* **FR4: LLM-Powered Content Generation for Mailchimp Context (MVP Scope)**

  * Integrate with an LLM API (Anthropic Claude for MVP, with a pluggable design for other providers).
  * Generate relevant marketing content ideas (e.g., 2-3 email subject lines, 1 short paragraph of body copy, 1 campaign theme idea) based on a selected trend.
  * Display generated content in a UI panel with copy-to-clipboard functionality.

## 3. Non-Functional Requirements (MVP)

* **NFR1: Performance (MVP Focus):** Dashboard interactivity \< 5-10s initial load, \< 3-5s filter changes. Data ingestion near real-time for demo (e.g., every 10-15 mins or on-demand).
* **NFR2: Scalability & Cloud-Readiness (MVP Design Consideration):** MVP architecture designed for scalability using Docker, local orchestration with Colima/k3s, and pluggable modules. Setup mirrors cloud-native patterns.
* **NFR3: Availability (MVP Context):** System needs to be stable for the 3-4 day prototype and demo. 99.9% availability is a post-MVP goal.
* **NFR4: Data Privacy & Compliance (MVP Awareness):** Handles publicly available news data. No PII from dashboard users stored. Respect `robots.txt` via Jina.
* **NFR5: Cost Efficiency (MVP Development):** Prioritize free-tier/low-cost services (Jina "r." calls, LLM free/dev tiers).
* **NFR6: Maintainability & Documentation (MVP Process):** Clean, organized, commented code for prototype. README for running.
* **NFR7: Usability (Dashboard MVP):** Intuitive dashboard, Mailchimp-aligned UI, clear data presentation.
* **NFR8: Security (MVP Basics):** Basic security for internal APIs. Secure management of external API keys (LLM).
* **NFR9: Testability & CI/CD Pipeline (MVP Foundation):** Unit/integration tests for core logic. Basic CI/CD (GitHub Actions) for automated builds of containers and running tests. Mock data plugin for robust testing.

## 4. User Interaction and Design Goals (MVP Dashboard)

* **Overall Vision & Experience:**
  * Clear, scannable, visually appealing dashboard enabling quick insights. Responsive and intuitive.
  * **Crucially, the design should strive to align with Mailchimp's established UI/UX patterns and aesthetics (clarity, approachability, similar layout paradigms, color cues). The long-term vision is for this engine to feel like an integrated part of the Mailchimp application.**
* **Key Interaction Paradigms:**
  * Trend Discovery: View list/grid of trends (Mailchimp-familiar presentation).
  * Filtering: By category/sentiment using Mailchimp-like interaction patterns.
  * Visualization Engagement: Interact with time-series charts (style complementary to Mailchimp).
  * LLM Content Generation: Trigger AI content idea generation for a trend; display in a panel with copy-to-clipboard. This interaction should feel like a natural extension.
* **Core Screens/Views (Conceptual for MVP):**
  * **Main Dashboard (SPA):** Structured like a Mailchimp page. Displays trend list/cards, visualizations, filters, and LLM content generation section.
* **Branding Considerations (High-Level):**
  * Achieve a look and feel harmonious with the Mailchimp application, referencing Mailchimp's design language (typography, iconography, spacing, color palette from user guide or app).
* **Accessibility Aspirations (MVP):** Clear, legible fonts, sufficient color contrast, following Mailchimp's practices.
* **Target Devices/Platforms:** Web application, desktop-optimized for demo, aiming for mobile-friendliness.

## 5. Technical Assumptions

* **A. Repository & Service Architecture:**
  * **Repository Structure: Monorepo**
    * **Rationale:** Simplify setup, facilitate cross-component refactoring, unified CI/CD for MVP.
    * **Structure:** Top-level `frontend` and `backend` directories.
  * **High-Level Service Architecture: "Majestic Monolith" for Backend; Separate Frontend**
    * **Rationale:** Backend as a single FastAPI application with clear internal modules (data ingestion, trend processing, API, LLM integration) for MVP simplicity, designed for future evolution to microservices. Frontend is a separate Next.js application.
* **B. Technology Stack & Libraries:**
  * **Frontend:** TypeScript, Next.js, Tailwind CSS, shadcn/ui (or similar), `pnpm` for package management.
  * **Backend (Python):** `uv` for env management, `src/mailchimp_trends/` layout, FastAPI, HTTPX. Jina AI Reader API (direct "r." calls, "s." calls with key for secondary search). Anthropic Claude API for LLM content generation (MVP), with a pluggable design for other LLMs.
  * **Containerization & Orchestration:** Docker, Colima with k3s locally, GitHub Actions with k3s for CI/CD.
* **C. Testing Requirements:** Unit tests for backend modules and frontend components. CI/CD integration for automated builds and tests. Mock Data Source Plugin for testing.
* **D. Development & Deployment:** MVP developed and demoed on Colima/k3s. Cloud-ready design.

## 6. [OPTIONAL: For Simplified PM-to-Development Workflow Only] Core Technical Decisions & Application Structure

* **Technology Stack Selections:**

  * **Primary Backend Language/Framework:** Python / FastAPI
  * **Primary Frontend Language/Framework:** TypeScript / Next.js
  * **Database (for MVP & initial processed data):** Simple file-based storage on Docker volumes or SQLite. (Full data warehouse is post-MVP).
  * **Key Libraries/Services (Backend):** `uv`, `httpx`, `anthropic` (Claude SDK), `pytest`, NLP libraries (e.g., spaCy, Hugging Face Transformers), `APScheduler` (or similar for scheduling).
  * **Key Libraries/Services (Frontend):** `pnpm`, Tailwind CSS, shadcn/ui (or similar), Chart.js (or similar), Jest/React Testing Library.
  * **Deployment Platform/Environment (for MVP development & demo):** Docker containers orchestrated by Colima/k3s locally.
  * **Version Control System:** Git with GitHub.

* **Proposed Application Structure (Conceptual Monorepo):**

    ```plaintext
    /── backend/
    │   ├── src/mailchimp_trends/
    │   │   ├── main.py             # FastAPI app entry point
    │   │   ├── api/                # API routers/endpoints
    │   │   ├── core/               # Core logic, config, constants
    │   │   ├── data_ingestion/     # Jina integration, scheduling
    │   │   ├── nlp_processing/     # NLP pipeline, topic, sentiment
    │   │   ├── trend_identification/ # Trend algorithms
    │   │   ├── llm_integration/    # Claude (pluggable LLM service)
    │   │   └── models/             # Pydantic models, data structures
    │   ├── tests/
    │   ├── Dockerfile
    │   └── pyproject.toml
    ├── frontend/
    │   ├── app/                  # Next.js app directory structure
    │   ├── components/
    │   ├── public/
    │   ├── styles/
    │   ├── Dockerfile
    │   ├── package.json
    │   └── pnpm-lock.yaml
    ├── .github/workflows/        # CI/CD pipeline (e.g., main.yml)
    ├── .gitignore
    ├── docker-compose.yml        # (Optional, if k8s manifests are preferred directly for Colima)
    ├── kubernetes/               # k8s manifests for local Colima/k3s deployment
    └── README.md
    ```

* **Key Modules/Components and Responsibilities:** (As outlined in backend `src` structure and frontend structure).

* **Data Flow Overview (Conceptual):**

    1. Scheduler (backend) triggers Data Ingestion Module.
    2. Data Ingestion Module calls Jina AI Reader for news sites -\> Raw text stored.
    3. NLP Processing Module takes raw text -\> Cleans, extracts topics, sentiment -\> Stores processed data.
    4. Trend Identification Module uses processed data -\> Calculates trend scores -\> Stores identified trends.
    5. Frontend (Next.js) calls Backend API Module for trends.
    6. Backend API Module fetches identified trends for dashboard display.
    7. Frontend user requests LLM content for a trend.
    8. Backend API Module calls LLM Integration Module.
    9. LLM Integration Module prompts Claude -\> Returns generated content to Frontend.

## 7. Epic Overview

* **Epic 1: Foundation & Core Backend Setup**

  * **Goal:** Establish the foundational backend application, CI/CD pipeline, local development environment (Docker, Colima/k3s), and basic API structure.
  * **Story 1.1: Project Scaffolding & Monorepo Setup**
    * **ACs:** Git repo, `frontend`/`backend` dirs, README, .gitignore.
  * **Story 1.2: Backend "Majestic Monolith" (FastAPI) Application Setup**
    * **ACs:** `uv`, `pyproject.toml`, `src/mailchimp_trends/`, FastAPI, `/health` endpoint, Dockerfile, runnable image.
  * **Story 1.3: Frontend (Next.js) Application Setup with `pnpm`**
    * **ACs:** Next.js, TypeScript, `pnpm`, Tailwind CSS, basic page, Dockerfile, runnable image.
  * **Story 1.4: Local Orchestration & Initial Frontend-Backend Connectivity (Colima/k3s)**
    * **ACs:** Colima/k3s setup docs, k8s manifests, services accessible, frontend calls backend `/health` & displays status/handles errors.
  * **Story 1.5: Basic CI/CD Pipeline with Build & Linting (using `pnpm`)**
    * **ACs:** GitHub Actions workflow (triggers, checkout, backend lint, frontend lint with `pnpm`, Docker builds for both, pipeline fails on errors).
  * **Story 1.6: Backend and Initial Frontend Connectivity Testing Framework & CI Integration**
    * **ACs:** `pytest` for backend, `/health` unit test. Jest/RTL for frontend. Frontend tests for `/health` call success/failure (mocked). CI runs all tests, fails on test failures.

* **Epic 2: Data Ingestion & Initial Processing**

  * **Goal:** Implement the ability to fetch content from news sources using Jina AI Reader, process this raw text, and store it in a preliminary format suitable for NLP analysis.
  * **Story 2.1: Configure News Sources & Basic Jina AI Reader Integration**
    * **ACs:** Configurable news URLs, backend module for Jina AI Reader (direct `r.jina.ai/URL` call, no key), parse response for text, error handling, unit test for fetching.
  * **Story 2.2: Scheduled or Triggered Article Fetching**
    * **ACs:** Scheduler (e.g., APScheduler or manual trigger API for MVP), iterates sources (simplified: re-fetches main page content or fixed article URLs), logging.
  * **Story 2.3: Raw Content Storage (Preliminary)**
    * **ACs:** Simple storage (files on Docker volume for MVP), stores full text, source URL, timestamp. Interface for NLP module to retrieve. Avoid re-processing identical content (basic check).
  * **Story 2.4: Mock Data Ingestion Plugin Refinement**
    * **ACs:** Mock plugin provides realistic raw article text + metadata, matching Jina output format. Consumable by NLP pipeline.

* **Epic 3: Trend Identification & NLP Core**

  * **Goal:** Develop the core NLP capabilities (topic extraction, sentiment analysis) and implement the initial algorithms to identify and score potential marketing trends from the processed data.
  * **Story 3.1: Basic NLP Preprocessing**
    * **ACs:** Backend NLP module. Steps: cleaning, tokenization, stop word removal, lemmatization/stemming (using spaCy or NLTK). Output is clean, tokenized text. Unit tests.
  * **Story 3.2: Topic Extraction/Modeling**
    * **ACs:** Integrate pre-trained Hugging Face transformer for topic modeling. Input: preprocessed text. Output: list of topics/keywords. Store topics. Basic unit tests.
  * **Story 3.3: Basic Sentiment Analysis**
    * **ACs:** Integrate pre-trained Hugging Face model for sentiment. Input: preprocessed text or topic snippets. Output: sentiment score (pos/neg/neu). Store sentiment. Unit tests.
  * **Story 3.4: Marketing Relevance Assessment (Initial Pass)**
    * **ACs:** Configurable marketing keyword list. Function compares topics against ontology. Flag/score relevant topics. Store relevance. Design for secondary search (post-MVP). Unit tests.
  * **Story 3.5: Trend Identification Algorithm (Frequency & Growth Rate - MVP)**
    * **ACs:** Aggregate marketing-relevant topic data. Calculate frequency & basic growth rate. Compute trend score. Store identified trends (topic, score, sentiment) for API. Unit tests with mock historical data.

* **Epic 4: Dashboard & Trend Visualization**

  * **Goal:** Create the Next.js frontend application to display the identified marketing trends, allow basic filtering, and visualize trend evolution, aligning with Mailchimp's UI style.
  * **Story 4.1: Basic Dashboard Layout & API Connection**
    * **ACs:** Next.js main page, Mailchimp-aligned layout (Tailwind), connects to backend `/api/v1/trends`, displays trend names/placeholders, basic error handling, responsive hint.
  * **Story 4.2: Trend Display with Key Information**
    * **ACs:** Each trend rendered (card/list) with name, date, sentiment, score. Mailchimp-aligned style. Sortable by one criterion (recency/score).
  * **Story 4.3: Trend Filtering (Basic)**
    * **ACs:** UI controls for filtering by category/sentiment. Updates list without full reload. Mailchimp-style controls.
  * **Story 4.4: Time-Series Visualization of Trend Evolution**
    * **ACs:** Charting library integrated. Backend API for trend history. Displays chart for selected trend (frequency/score over time). Interactive chart. Mailchimp-aligned style.
  * **Story 4.5: Frontend Unit & Integration Tests for Dashboard Components**
    * **ACs:** Unit tests for components (Jest/RTL). Tests cover rendering with mock data, basic interactions. CI runs tests.

* **Epic 5: LLM Content Generation & MVP Polish**

  * **Goal:** Implement LLM-powered (Claude) content generation for Mailchimp context and conduct final testing and polishing of the end-to-end MVP flow.
  * **Story 5.1: Backend LLM Integration Design (Pluggable) & Claude Setup**
    * **ACs:** Generic LLM service interface defined. `ClaudeLLMService` implementation created. Anthropic Claude SDK added. Secure API key config. Basic test call to Claude API successful. Error handling. Unit tests for `ClaudeLLMService`.
  * **Story 5.2: Claude-Powered Marketing Content Generation Logic**
    * **ACs:** Backend API endpoint (`/api/v1/trends/{trend_id}/generate-content-ideas`). Retrieves trend details. Effective prompts engineered for Claude (subjects, body copy, themes). Calls `ClaudeLLMService`. Parses & structures response. API returns generated content. Unit tests (mocked Claude response).
  * **Story 5.3: Frontend UI for LLM Content Display & Copy-Paste**
    * **ACs:** UI button ("Generate Ideas with AI" / "Draft with Claude"). Calls backend API. Loading state. Displays generated content in panel/modal. "Copy to Clipboard" function. UI feedback. Mailchimp-aligned style.
  * **Story 5.4: End-to-End MVP Testing & Polish (with Claude Content Generation)**
    * **ACs:** Full user flow tested (ingestion -\> trends -\> dashboard -\> Claude content -\> copy). Bugs/UI issues addressed. Acceptable demo performance. README updated with LLM key setup. All services run in Colima/k3s.

## 8. Key Reference Documents

(This section would typically list external documents. For this exercise, primary references are the user's initial project brief and this PRD itself. The Mailchimp User Guide PDF also serves as a UI style reference.)

* Mailchimp Marketing Trends Engine: Design & Development Prompt (User Provided)
* Mailchimp User Guide (User Provided PDF - for UI/UX alignment reference)
* Jina AI Documentation (for Reader & Search APIs)
* Anthropic Claude Documentation (for LLM API)
* Next.js, FastAPI, Docker, Kubernetes (k3s), Tailwind CSS, etc., official documentations.

## 9. Out of Scope Ideas Post MVP

* Crawlers for specific social media platforms (Twitter, LinkedIn, Instagram) requiring authenticated APIs and complex data extraction.
* Advanced trend identification algorithms (e.g., deep cross-platform correlation, advanced user engagement metric analysis).
* Predictive analytics for trend forecasting.
* Full, live Mailchimp API integration for direct campaign creation/modification beyond the conceptual design and LLM-generated copy/paste content.
* Public/Third-party developer API for the Trends Engine.
* Advanced user management, roles, and permissions for the dashboard.
* Comprehensive data warehousing solution beyond MVP's simple storage.
* Full multi-language support for trend analysis and UI.
* Automated secondary research an FR1.5 (full implementation).
* Integration with other LLM providers beyond the initial Claude setup (though architecture supports it).

## Change Log

| Change             | Date          | Version | Description                                     | Author                        |
| :----------------- | :------------ | :------ | :---------------------------------------------- | :---------------------------- |
| Initial PRD Draft  | May 16, 2025  | 1.0     | First complete draft based on collaborative input | 2-pm (AI Product Manager)     |
