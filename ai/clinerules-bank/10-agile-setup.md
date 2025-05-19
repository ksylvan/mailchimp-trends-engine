# Agile Process Guide for Mailchimp Marketing Trends Engine

When working on the Mailchimp Marketing Trends Engine project, please adhere to the following Agile process guidelines:

1. **Understand Project Structure:**
   * The project is broken down into Epics and User Stories. These are documented in Markdown files located in the `./ai/agile/` directory.
   * Familiarize yourself with the naming convention (e.g., `epic-X_story-Y.Z_description.md`).

2. **Focus on User Stories:**
   * Each story file typically contains:
     * A "Story" section describing the user need.
     * A set of "Acceptance Criteria (ACs)".
   * **Your primary focus for development must be to meet all Acceptance Criteria for the assigned story.**

3. **Refer to Project Documentation:**
   * Detailed project documentation (PRD, architecture, UI/UX specs, etc.) is available in the `./docs/` directory.
   * Consult these documents as needed to gain context and ensure your work aligns with the overall project goals and technical specifications.

4. **Development and Implementation:**
   * Implement solutions directly related to the Acceptance Criteria of the current story.
   * If a story involves creating new files or modifying existing ones, ensure paths and naming conventions align with project standards (refer to existing structure and documentation).
   * For stories involving specific technologies or frameworks (e.g., FastAPI, Next.js, Kubernetes, Jina AI, Hugging Face Transformers, Anthropic Claude), ensure your implementation aligns with the choices outlined in the architecture documents and story ACs.

5. **Communication and Updates:**
   * When you complete work on a story, clearly state how the Acceptance Criteria have been met.
   * If you encounter ambiguities or blockers related to a story or its ACs, please ask for clarification.
   * Keep the checklists in the story file that you are working on updated.
   * A Task is only completed when it passes all the tests associated with it.

By following these guidelines, you will help ensure that development proceeds efficiently and aligns with the project's agile framework and objectives.
