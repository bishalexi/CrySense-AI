document.addEventListener("DOMContentLoaded", () => {
  const loginForm = document.getElementById("loginForm");
  const registerForm = document.getElementById("registerForm");

  // Demo login validation.
  // This is front-end only and does NOT provide real authentication.
  if (loginForm) {
    loginForm.addEventListener("submit", (event) => {
      event.preventDefault();

      const email = document.getElementById("loginEmail").value.trim();
      const password = document.getElementById("loginPassword").value;
      const message = document.getElementById("loginMessage");

      if (!email || !password) {
        message.textContent = "Please enter email and password.";
        message.style.color = "#c0392b";
        return;
      }

      message.textContent = "Login successful (demo).";
      message.style.color = "#16834b";
    });
  }

  // Demo registration validation.
  if (registerForm) {
    registerForm.addEventListener("submit", (event) => {
      event.preventDefault();

      const password = document.getElementById("registerPassword").value;
      const confirmPassword = document.getElementById("confirmPassword").value;
      const message = document.getElementById("registerMessage");

      if (password.length < 6) {
        message.textContent = "Password must contain at least 6 characters.";
        message.style.color = "#c0392b";
        return;
      }

      if (password !== confirmPassword) {
        message.textContent = "Passwords do not match.";
        message.style.color = "#c0392b";
        return;
      }

      message.textContent = "Registration successful (demo).";
      message.style.color = "#16834b";
    });
  }
});

function forgotPassword(event) {
  event.preventDefault();
  alert("Password reset can be connected to your backend later.");
}
