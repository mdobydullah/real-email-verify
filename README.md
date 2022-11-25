# Flask Email Verifier



## Installation & Usage

To use this project, start by cloning the repository:

```bash
git clone https://github.com/mdobydullah/flask-email-verifier.git
```

cd into the project, and make a copy of `.env_example` to `.env`

```bash
$ cp .env.example .env
```

### Build and Run

You can run the application stack (Flask application and Redis) with Docker, respectively docker-compose.

```docker
docker-compose up -d --build
```

Now visiti the URL:

```bash
http://localhost:5000/
```

You'll see the output:

```json
{
  success: true,
  message: "Welcome to Flask Email Verifier!",
  powered_by: "https://shouts.dev/"
}
```

#### Remove

```docker
docker-compose down -v
```

### Test the Application

#### Verify an email:

```bash
http://localhost:5000/verify?email=hi@obydul.me
```

Response:

```json
{
  "success": true,
  "send_from": "noreply@gmail.com",
  "send_to": "hi@obydul.me",
  "domain": "obydul.me",
  "mx_record": "alt1.aspmx.l.google.com.",
  "mx_cached": true,
  "response_code": 250,
  "message": "b'2.1.5 OK my13-20020a17090b4c8d00b00218a592ceacsi7016111pjb.107 - gsmtp'"
}
```

#### Available query parameters:

```bash
from & email

http://localhost:5000/verify?from=EMAIL_ADDESS&email=EMAIL_ADDESS
```

### License

This project is licensed under the terms of the MIT license.
