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
                window.location.href = '/';
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

async function loginUser(email, password) {
    const apiUrl = '/auth/login';
    const userData = {
        email,
        password,
    };
    const response = await fetch(apiUrl, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(userData),
    });

    console.log(response);

    if (response.redirected) {
        window.location.href = response.url; // Redirect to the home page
    } else {
        const Data = await response.json();
        if (Data) {
            alert(`Login unauthorized, (${Data.message})`);
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
    if (!email.match(/^\w+@\w+\.\w+$/i)) {
        alert('Invalid email address');
        return;
    }
    registerUser(username, email, password, status);
}

function handleLogin() {
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;

    if (!email || !password) {
        alert("Please fill in all fields!");
        return;
    }
    if (!email.match(/^\w+@\w+\.\w+$/i)) {
        alert('Invalid email address');
        return;
    }
    loginUser(email, password);

}

document.querySelector('.bxl-microsoft').addEventListener('click', function () {
    document.querySelector('.login .input-box:nth-child(2)').style.display = 'none';
    document.querySelector('.login .btn').style.display = 'none';
    document.getElementById('email-verification-box').style.display = 'block';
    document.getElementById('verification-code-box').style.display = 'none';
    document.getElementById('send-code-btn').style.display = 'block';
    document.getElementById('verification-code').style.display = 'none';
    document.getElementById('password-login').style.display = 'none';
    document.getElementById('email-login').style.display = 'block';
    document.getElementById('verify-code-btn').style.display = 'none';
});

document.querySelector('.bx-left-arrow-alt').addEventListener('click', function () {
    document.querySelector('.login .input-box:nth-child(2)').style.display = 'block';
    document.querySelector('.login .btn').style.display = 'block';
    document.getElementById('email-verification-box').style.display = 'none';
    document.getElementById('send-code-btn').style.display = 'none';
    document.getElementById('password-login').style.display = 'block';
    document.getElementById('email-login').style.display = 'none';
});

async function sendCode(email){
    const apiUrl = '/email/code/send';

    const userData = {
        email
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
                return true;
            default:
                alert(`Error, (${Data.message})`);
                return false;
        }
    }
    else {
        alert('Error, Network Error');
        return false;
    }
}

async function authenticateCode(email, verification_code){
    const apiUrl = '/email/code/login';

    const userData = {
        email,
        verification_code
    };

    const response = await fetch(apiUrl, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(userData),
    });

    if (response.redirected) {
        window.location.href = response.url; // Redirect to the home page
    } else {
        const Data = await response.json();
        if (Data) {
            alert(`Login unauthorized, (${Data.message})`);
        }
    }
}


function sendVerificationCode() {
    const email = document.getElementById('verification-email').value;
    if (!email.match(/^\w+@\w+\.\w+$/i)) {
        alert('Invalid email address');
        return;
    }

    console.log(sendCode(email));
    

    if(!sendCode(email)){
        alert('Verification code sent failed, please try again');
        return;
    }

    alert('Verification code sent to ' + email);
    
    document.getElementById('send-code-btn').style.display = 'none';
    document.getElementById('verification-code-box').style.display = 'block';
    document.getElementById('verification-code').style.display = 'block';
    document.getElementById('verify-code-btn').style.display = 'block';
}

function verifyCode() {
    const code = document.getElementById('verification-code').value;
    const email = document.getElementById('verification-email').value;

    authenticateCode(email, code);
}