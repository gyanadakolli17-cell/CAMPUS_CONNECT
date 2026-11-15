CAMPUS CONNECT - FRONTEND STARTER
=================================

Included:
- information.html     Information section
- ask-seniors.html     Ask Seniors listing page
- seniors.html         Senior mentor directory with sample profile cards
- projects.html        Projects showcase
- style.css            Shared design system and responsive styling
- app.js               Mobile navigation and sample filters

DESIGN DIRECTION
The pages follow the supplied reference video:
- Dark navy top navigation
- Light cool-grey page background
- White rounded content cards
- Cobalt-blue primary buttons
- Clean DM Sans typography
- Restrained spacing, subtle borders and shadows
- Responsive layouts for mobile and desktop

HOW TO RUN
1. Extract this ZIP.
2. Open the extracted folder in VS Code.
3. Keep the HTML pages, style.css and app.js together in the same folder.
4. Open index.html with Live Server and use the navigation links to explore.
5. Submit any valid email and password on login.html to enter the mock
   Senior Directory, or open seniors.html directly.

IMPORTANT INTEGRATION NOTES
1. These are frontend starter pages with sample content. They do not include a database or real authentication. The login form is a frontend-only demo and accepts any valid email and password.
2. Ask Seniors questions and project-interest requests are frontend demos only: new questions appear on the current page until reload, while interest details are not sent or stored. Connect these forms to the agreed backend before treating submissions as live.
3. Replace the sample senior profiles with verified campus mentor information.
4. Connect the "Log in", "Join the community", "Ask a question" and "Share your project" links to your actual login, registration and submission routes.
5. If your team already has a shared navbar, footer or CSS file, merge these styles rather than creating duplicate versions.
6. If the existing project uses Django, Flask, Java or another backend, your team should adapt the href paths and template syntax to its routing structure.
7. Do not overwrite your existing dashboard or backend files. Copy these pages into a backup/new branch first and integrate carefully.

SUGGESTED TEAM HANDOFF
- Objective 1: information.html + shared navbar styles
- Objective 2: ask-seniors.html + question list/filter structure
- Objective 3: style.css + shared header/footer/buttons/colour tokens
- Objective 4: projects.html + projects navigation link

The sample questions and project descriptions are placeholders for layout demonstration. Replace them with verified Campus Connect content before final submission.
