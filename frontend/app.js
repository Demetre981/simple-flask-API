window.onload = (event) => {

    const routes = [
        {path: '/', handler: homeHandler},
        {path: '/index.html', handler: homeHandler},
        {path: '/login.html', handler: loginHandler},
        {path: '/signup.html', handler: signupHandler}
    ]

    handleUrlChange();


    function handleUrlChange () {
        const path = window.location.pathname;
        const urlPath = routes.find(route => route.path === path)

        if (urlPath) {
            urlPath.handler();

        } else {
            homeHandler();
        }
    }

    function homeHandler () {
        const eventForm = document.getElementById("event-form");
        const urlAddEvent = 'http://127.0.0.1:5000/create_event';
        const date = new Date().toISOString();

        getEventsByDate(date);
    }

    function loginHandler () {
        console.log("Login")
    }

    function signupHandler () {
        console.log("Signup")
    }


    const urlLogin = 'http://127.0.0.1:5000/login';
    const urlSignup = 'http://127.0.0.1:5000/signup';


    function getEventsByDate (date) {
        const apiUrlGet = `http://127.0.0.1:5000/get_events_by_date/${date}`;

        fetch(apiUrlGet, {
            method: "GET",})
          .then(response => response.json())
          .then(data => {
            console.log(data);
          })
          .catch(error => {
            console.error('Помилка:', error);
          });
    }




    const signupForm = document.getElementById("signup-form");
    const loginForm = document.getElementById("login-form");

    if (eventForm) {
        sendRequestToServer(eventForm, urlAddEvent);
    }

    function sendRequestToServer (form, url) {

        form.addEventListener("submit", (event) => {
        event.preventDefault();

        const formData = new FormData(form);
        const data = {};

        for (const[key, value] of formData.entries()) {
            data[key] = value;
        }

        fetch(url, {
            method: "POST",
            headers: {"Content-type": "application/json"},
            body: JSON.stringify(data)
        })
        .then(data => console.log(data))
        .catch(error => console.error('Помилка:', error));
    })
    }
}

