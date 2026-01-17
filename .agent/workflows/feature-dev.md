---
description: Feature Development Workflow
---

1. Analyze: Read the task and identify necessary component changes.
2. Plan: Create an implementation plan (Artifact).
3. Code: Use Aider/Tool to implement changes.
4. Verify:
    - Run npm run type-check.
    - Run npm run lint.
    - Run npm test.
5. Refactor: If any verification step fails, fix errors and retry (max 3 attempts).
6. Browser Check: Launch browser, navigate to the page, and take a screenshot Artifact.

