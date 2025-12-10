---
description: How to update C4 architecture diagrams
---

This workflow describes the process for updating the C4 architecture diagrams located in `docs/architecture/` when the system design changes.

## When to Run
Run this workflow before requesting a version tag if you have:
- Added, removed, or renamed an agent.
- Changed external dependencies (e.g., new API).
- Altered the high-level project structure.

## Steps

### 1. Identify the Scope of Change
- **System Context (`system_context.mmd`)**: Did we add a new external user or system (e.g., a new API)?
- **Container (`container.mmd`)**: Did we add a new major component (e.g., a web UI, a database)?
- **Component (`component.mmd`)**: Did we add/remove/change an agent or a tool?

### 2. Update the Diagrams
Edit the `.mmd` files in `docs/architecture/` using the Mermaid syntax.

#### component.mmd (Common Case)
If you added an agent:
1.  Open `docs/architecture/component.mmd`.
2.  Add the new agent node inside the `Workers` subgraph.
3.  Add the reporting lines from the `Manager`.
4.  Add the flow lines to/from other agents.

### 3. Verify
Ensure the diagrams render correctly. You can:
- Use the Mermaid preview in your IDE.
- Paste the code into [Mermaid.live](https://mermaid.live).

### 4. Commit
Commit the changes along with your code updates.
