## Best Practices for Team AI Use on HTML Dashboards

### 1. Define Goal and Context First
- Clarify the dashboard purpose, audience, and key metrics before asking for AI assistance.
- Provide the product context, design system, and component conventions when requesting HTML/CSS suggestions.
- Define the desired interactivity up front, including dropdown filters, controls, and interactive widgets.
- Specify that every chart should include a header, and note the typography expectations: headers in Georgia 22 pt and content in Arial 14 pt.
- Use AI for specific deliverables like markup patterns, layout options, or accessible widget ideas.

### 2. Keep Output Modular and Reviewable
- Request isolated UI snippets (cards, tables, chart containers) instead of full-page code.
- Review generated HTML for semantic structure, responsive behavior, and maintainability.
- Use team reviews and code review workflows as the final quality gate.

### 3. Honor Existing Team Style and Patterns
- Share naming conventions, CSS class patterns, and the component library in prompts.
- Normalize AI-generated code to the team’s HTML, CSS, and JavaScript standards.
- Avoid introducing new patterns unless the team agrees to adopt them.

### 4. Treat AI as a Drafting Partner
- Accept AI output as a starting point, not a finished product.
- Validate generated dashboard code for accessibility, performance, and compatibility.
- Run outputs through the same linting, formatting, and testing pipelines used by the team.

### 5. Document Prompts and Decisions
- Keep a shared prompt log for useful AI queries and successful dashboard patterns.
- Record why a particular AI suggestion was accepted, revised, or rejected.
- Use this shared knowledge to improve future prompts and consistency.

### 6. Protect Data and Privacy
- Never include private business metrics, API keys, or sensitive dashboard data in prompts.
- Use anonymized or sample data when requesting dashboard layout or visualization code.
- Confirm generated code does not expose internal endpoints or credentials.

### 7. Collaborate Actively
- Review AI-generated HTML in team meetings or design reviews before implementation.
- Encourage teammates to comment on generated markup and suggest improvements.
- Align on when AI should be used for ideation, scaffolding, or debugging.

### 8. Prioritize Accessibility and UX
- Ask AI to include semantic elements, ARIA labels, keyboard support, and alt text.
- Verify generated dashboard patterns against accessibility standards before launch.
- Use AI to help suggest inclusive designs, but keep the final check human-led.

### 9. Iterate with Feedback
- Use AI to explore multiple dashboard layout or interaction options quickly.
- Gather team and user feedback, then refine prompts and generated code.
- Focus on real user needs and team-maintained design consistency.

### 10. Keep Humans in Control
- Always have a developer or designer validate AI-generated dashboard work.
- Use AI as a productivity partner, not the final decision-maker.
- Make final implementation decisions based on team standards and maintainability.
