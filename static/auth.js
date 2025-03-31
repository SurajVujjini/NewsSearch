function handleCredentialResponse(response) {
    const userInfo = decodeJwtResponse(response.credential);
    document.getElementById('user-info').style.display = 'block';
    document.getElementById('user-image').src = userInfo.picture;
    document.getElementById('user-name').textContent = userInfo.name;
    document.getElementById('user-email').textContent = userInfo.email;
    
    // Send the token to your server
    fetch('/auth', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({credential: response.credential})
    });
}

function decodeJwtResponse(token) {
    const base64Url = token.split('.')[1];
    const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
    return JSON.parse(window.atob(base64));
}

function signOut() {
    google.accounts.id.disableAutoSelect();
    document.getElementById('user-info').style.display = 'none';
    fetch('/logout', {
        method: 'POST'
    });
}
