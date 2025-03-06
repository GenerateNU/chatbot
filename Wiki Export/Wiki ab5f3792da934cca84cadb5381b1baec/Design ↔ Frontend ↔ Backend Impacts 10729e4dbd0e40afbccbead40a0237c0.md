# Design ↔ Frontend ↔ Backend Impacts

Author: frank, erin, Brian Reicher
Branch: Software
Hidden: No
Parent page: Breaking Silos (Breaking%20Silos%202d26a01f9689444bbb069f20491b80ac.md)

### 🎨 Changes other members of the team can make which impact ***designers***:

- 🖥️ 👍 Request design QA as needed and in advance

### 🖥️ Changes other members of the team can make which impact ***frontend-focused developers***:

- 🎨 👍 A component library is built into a Figma page since it makes it simpler to translate designs to implementation
- 🎨 👍 Mockups are shared early and often so that engineering work can begin setting up while design work moves to polishing-focused stages
- 🎨 👍 Even when not included in the designs, it’s useful to have discussions of additional user interactions such as animation, hover states, etc. which can be added to components and implemented across the project to “bring it to life”
- 🤖 👍 Endpoints remain stable in both setup and contents, and mask implementation details, so that changes to the backend do not impact the frontend
- 🤖 👍 Types (where possible) are shared across the codebase to remove complexity and need for duplication of work.

### 🤖 Changes other members of the team can make which impact ***backend-focused developers***:

- 🎨 👍 Important to have a shared understanding of how data is likely to expand in scope over time