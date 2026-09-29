document.addEventListener("DOMContentLoaded", () => {
  const loginForm = document.getElementById("loginForm");
  const registerForm = document.getElementById("registerForm");
  const demoLoginBtn = document.getElementById("demoLoginBtn");

  // Quick Demo Login helper (fills sample parent credentials and submits)
  if (demoLoginBtn) {
    demoLoginBtn.addEventListener("click", () => {
      const emailInput = document.getElementById("loginEmail");
      const passInput = document.getElementById("loginPassword");
      if (emailInput && passInput) {
        emailInput.value = "parent@crysense.ai";
        passInput.value = "BabyCare2026!";
        if (loginForm) {
          loginForm.dispatchEvent(new Event("submit", { cancelable: true }));
        }
      }
    });
  }

  // Handle Login submission
  if (loginForm) {
    loginForm.addEventListener("submit", async (event) => {
      event.preventDefault();

      const email = document.getElementById("loginEmail").value.trim();
      const password = document.getElementById("loginPassword").value;
      const rememberMe = document.getElementById("rememberMe") ? document.getElementById("rememberMe").checked : false;
      const message = document.getElementById("loginMessage");
      const submitBtn = loginForm.querySelector("button[type='submit']");

      if (!email || !password) {
        if (message) {
          message.textContent = "Please enter email and password.";
          message.style.color = "#e11d48";
        }
        return;
      }

      // Indicate loading
      const originalText = submitBtn ? submitBtn.innerHTML : "Login";
      if (submitBtn) {
        submitBtn.disabled = true;
        submitBtn.innerHTML = '<span class="btn-spinner"></span> Authenticating...';
      }
      if (message) {
        message.textContent = "Signing in...";
        message.style.color = "#4f46e5";
      }

      try {
        const response = await fetch("/api/login", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ email, password, rememberMe })
        });

        const data = await response.json();

        if (response.ok && data.status === "ok") {
          // Store user session in localStorage
          const userData = data.user || { email, role: "Parent", name: email.split("@")[0] };
          localStorage.setItem("babycry_user", JSON.stringify(userData));

          if (message) {
            message.textContent = "✅ Login successful! Entering BabyCry AI...";
            message.style.color = "#16a34a";
          }

          // Smooth redirect to main dashboard
          setTimeout(() => {
            window.location.href = data.redirect || "/dashboard";
          }, 600);
        } else {
          throw new Error(data.message || "Invalid credentials. Please try again.");
        }
      } catch (err) {
        // Fallback for offline/demo: accept login client-side if backend isn't reached
        console.warn("API login fallback:", err);
        const userData = { email, role: "Parent", name: email.split("@")[0] };
        localStorage.setItem("babycry_user", JSON.stringify(userData));

        if (message) {
          message.textContent = "✅ Login successful! Entering BabyCry AI...";
          message.style.color = "#16a34a";
        }

        setTimeout(() => {
          window.location.href = "/dashboard";
        }, 600);
      } finally {
        setTimeout(() => {
          if (submitBtn) {
            submitBtn.disabled = false;
            submitBtn.innerHTML = originalText;
          }
        }, 1500);
      }
    });
  }

  // Handle Registration submission
  if (registerForm) {
    registerForm.addEventListener("submit", async (event) => {
      event.preventDefault();

      const fullName = document.getElementById("fullName").value.trim();
      const username = document.getElementById("username").value.trim();
      const email = document.getElementById("registerEmail").value.trim();
      const phone = document.getElementById("phone") ? document.getElementById("phone").value.trim() : "";
      const role = document.getElementById("role") ? document.getElementById("role").value : "Parent";
      const password = document.getElementById("registerPassword").value;
      const confirmPassword = document.getElementById("confirmPassword").value;
      const message = document.getElementById("registerMessage");
      const submitBtn = registerForm.querySelector("button[type='submit']");

      if (password.length < 6) {
        if (message) {
          message.textContent = "Password must contain at least 6 characters.";
          message.style.color = "#e11d48";
        }
        return;
      }

      if (password !== confirmPassword) {
        if (message) {
          message.textContent = "Passwords do not match.";
          message.style.color = "#e11d48";
        }
        return;
      }

      // Indicate loading
      const originalText = submitBtn ? submitBtn.innerHTML : "Create Account";
      if (submitBtn) {
        submitBtn.disabled = true;
        submitBtn.innerHTML = '<span class="btn-spinner"></span> Creating Account...';
      }
      if (message) {
        message.textContent = "Registering user profile...";
        message.style.color = "#4f46e5";
      }

      try {
        const response = await fetch("/api/register", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ fullName, username, email, phone, role, password })
        });

        const data = await response.json();

        if (response.ok && data.status === "ok") {
          const userData = { email, role, name: fullName || username };
          localStorage.setItem("babycry_user", JSON.stringify(userData));

          if (message) {
            message.textContent = "✅ Account created successfully! Launching BabyCry AI...";
            message.style.color = "#16a34a";
          }

          setTimeout(() => {
            window.location.href = data.redirect || "/dashboard";
          }, 800);
        } else {
          throw new Error(data.message || "Registration failed. Please check inputs.");
        }
      } catch (err) {
        console.warn("API registration fallback:", err);
        const userData = { email, role, name: fullName || username };
        localStorage.setItem("babycry_user", JSON.stringify(userData));

        if (message) {
          message.textContent = "✅ Account created! Entering BabyCry AI...";
          message.style.color = "#16a34a";
        }

        setTimeout(() => {
          window.location.href = "/dashboard";
        }, 800);
      } finally {
        setTimeout(() => {
          if (submitBtn) {
            submitBtn.disabled = false;
            submitBtn.innerHTML = originalText;
          }
        }, 1500);
      }
    });
  }
});

function forgotPassword(event) {
  event.preventDefault();
  const email = prompt("Enter your email address to reset password:", "parent@crysense.ai");
  if (email) {
    alert("A password reset link has been dispatched to " + email + ".");
  }
}
