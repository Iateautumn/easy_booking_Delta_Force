const container = document.querySelector('.container')
const registerBtn = document.querySelector('.register-btn')
const loginBtn = document.querySelector('.login-btn')

registerBtn.addEventListener('click', () => {
  container.classList.add('active')
})

loginBtn.addEventListener('click', () => {
  container.classList.remove('active')
})

async function registerUser(username, email, password, status) {
  const apiUrl = '/auth/register';
  const userData = {
    username,
    email,
    password,
    status
  };
  const response = await fetch(apiUrl, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(userData),
  });

  const Data = await response.json();
  if (Data) {
    switch (Data.code) {
      case 200:
        alert('Register Success! Please login now!');
        window.location.href = '/login';
        break;
      case 400:
        alert(`Validation failed: ${Data.details?.join(', ') || 'Invalid parameters'}`);
        break;
      case 409:
        alert(`Resource conflict: ${Data.message || 'Duplicate username/email'}`);
        break;
      default:
        alert(`Internal server error (${Data.message})`);
    }
  }
}

function handleRegister() {
  const username = document.getElementById('registration-username').value;
  const email = document.getElementById('registration-email').value;
  const password = document.getElementById('registration-password').value;
  const status = document.getElementById('status').value;

  if (!username || !email || !password || status === "Select Your Identity...") {
    alert("Please fill in all fields!");
    return;
  }

  registerUser(username, email, password, status);

}
