function setCookie(name, value) {
  const secure = window.location.protocol === 'https:' ? '; Secure' : '';
  document.cookie = `${name}=${encodeURIComponent(value)}; Path=/; SameSite=Strict${secure}`;
}

function getCookie(name) {
  const cookie = document.cookie
    .split('; ')
    .find((entry) => entry.startsWith(`${name}=`));

  return cookie ? decodeURIComponent(cookie.slice(name.length + 1)) : null;
}

function deleteCookie(name) {
  const secure = window.location.protocol === 'https:' ? '; Secure' : '';
  document.cookie = `${name}=; Max-Age=0; Path=/; SameSite=Strict${secure}`;
}

function setCookies(sessionId, email) {
  if (!sessionId || !email) {
    throw new TypeError('Both sessionId and email are required.');
  }

  setCookie('session_id', sessionId);
  setCookie('email', email);
}

function redirectToDashboardIfSessionValid(validationUrl, dashboardUrl) {
  if (!getCookie('session_id') || !getCookie('email')) {
    return;
  }

  fetch(validationUrl, { credentials: 'same-origin' })
    .then((response) => {
      if (!response.ok) {
        throw new Error(`Session validation failed with status ${response.status}`);
      }
      return response.json();
    })
    .then((result) => {
      if (result.valid) {
        window.location.replace(dashboardUrl);
      } else {
        deleteCookie('session_id');
        deleteCookie('email');
      }
    })
    .catch((error) => {
      console.error('Unable to validate the session:', error);
    });
}

document.addEventListener('DOMContentLoaded', () => {
  const { sessionId, email } = document.body.dataset;

  if (sessionId && email) {
    setCookies(sessionId, email);
  } else if (document.body.dataset.redirectIfValidSession !== 'true') {
    deleteCookie('session_id');
    deleteCookie('email');
  }
});