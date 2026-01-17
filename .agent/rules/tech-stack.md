# Tech Stack Constraints
## React & TypeScript
- Use functional components only.
- Strict Type Safety: No any. Define interfaces for all Props. Use zod for validation if needed.
- State Management: Use React Context for local state, Zustand for global state.
- File Structure: Colocate tests with components (e.g., Button.tsx, Button.test.tsx).

## Tailwind CSS
- Use utility classes ONLY. Do not create .css files or use style={{}} props unless dynamic values (coordinates) are required.
- Use clsx and tailwind-merge for conditional class application.
- Follow the designated UI Kit (e.g., Shadcn/UI or Flowbite) tokens. Do not invent "magic values" (e.g., w-[342px]); use standard spacing (w-96).