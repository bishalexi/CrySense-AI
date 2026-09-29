BABYCRY SENSE AI - LOGIN & REGISTRATION UI

Files:
1. index.html       -> Login page
2. register.html    -> Registration page
3. style.css        -> Complete design and baby background
4. script.js        -> Demo form validation

HOW TO RUN:
- No installation is required.
- Put all four files in the same folder.
- Open index.html in Chrome, Edge, Firefox, or another modern browser.
- Click "Create Account" to open the registration page.
- In VS Code, install the "Live Server" extension and right-click index.html
  -> Open with Live Server.

IMPORTANT:
This is a front-end UI/demo. Login and registration are not connected to a
database yet. For real authentication, connect these forms to a backend such
as PHP + MySQL, Node.js + MySQL/MongoDB, Python Flask/Django, etc.

BABY IMAGE:
The CSS currently uses an online Unsplash baby image. If you want the project
to work completely offline, save your own baby image as "baby.jpg" inside the
same folder and change the background-image URL in style.css to:

background-image:
  linear-gradient(120deg, rgba(22, 25, 65, 0.58), rgba(88, 69, 120, 0.35)),
  url("baby.jpg");
