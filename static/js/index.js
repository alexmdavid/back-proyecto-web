document.getElementById('loginForm').addEventListener('submit', function(event) {
    event.preventDefault();
    validateForm();
});

function validateForm() {
    // Limpiar errores previos
    clearErrors();

    let isValid = true;

    // Validar email
    const email = document.getElementById('email');
    const emailError = document.getElementById('emailError');
    const emailPattern = /^[^ ]+@[^ ]+\.[a-z]{2,3}$/;

    if (email.value.trim() === '') {
        emailError.textContent = 'Email is required';
        emailError.style.display = 'block';
        email.parentElement.classList.add('error');
        isValid = false;
    } else if (!emailPattern.test(email.value)) {
        emailError.textContent = 'Please enter a valid email';
        emailError.style.display = 'block';
        email.parentElement.classList.add('error');
        isValid = false;
    }

    // Validar contraseña
    const password = document.getElementById('password');
    const passwordError = document.getElementById('passwordError');

    if (password.value.trim() === '') {
        passwordError.textContent = 'Password is required';
        passwordError.style.display = 'block';
        password.parentElement.classList.add('error');
        isValid = false;
    } else if (!isPasswordSecure(password.value)) {
        passwordError.textContent = 'Password must be at least 8 characters long and include uppercase, lowercase, and a number';
        passwordError.style.display = 'block';
        password.parentElement.classList.add('error');
        isValid = false;
    }

    if (isValid) {
        alert('Form Submitted Successfully');
    }
}

// Función para validar la seguridad de la contraseña
function isPasswordSecure(password) {
    // Al menos 8 caracteres, una letra mayúscula, una minúscula y un número
    const passwordPattern = /^(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,}$/;
    return passwordPattern.test(password);
}

function clearErrors() {
    const errors = document.querySelectorAll('small');
    errors.forEach(error => {
        error.style.display = 'none';
    });

    const inputs = document.querySelectorAll('.input-group');
    inputs.forEach(input => {
        input.classList.remove('error');
    });
}

// Función para alternar la visibilidad de la contraseña
const togglePassword = document.getElementById('togglePassword');
const passwordField = document.getElementById('password');

togglePassword.addEventListener('click', function() {
    // Verificar el tipo actual del input de contraseña
    const type = passwordField.getAttribute('type') === 'password' ? 'text' : 'password';
    passwordField.setAttribute('type', type);

    // Cambiar el ícono dependiendo del tipo
    this.textContent = type === 'password' ? '👁️' : '🙈';
});
