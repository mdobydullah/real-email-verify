<p align="center">
    <img src="https://cdn.shouts.dev/media/146/real-email-verify.png" alt="logo" width="100"/><br>
    <b>Real Email Verify</b>
</p>

## Features

* Syntax checker
* Domain verification
* MX (Mail Exchange records) verification
* Caching domain lookups to improve performance

## Installation

To use this project, start by cloning the repository:

```bash
git clone https://github.com/mdobydullah/real-email-verify.git
```

cd into the project, and make a copy of `.env.example` to `.env`

```bash
cp .env.example .env
```

### Build and Run

You can run the application stack (Flask application and Redis) with Docker, respectively docker-compose.

```docker
docker-compose up -d --build
```

Now visit the URL:

```bash
http://localhost:5000/
```

You'll see an input field. After submitting an email address, it'll show response like:

<p align="center">
    <img src="https://cdn.shouts.dev/media/149/rmv-index.png" alt='response'>
</p>

#### Stop Application

```docker
docker-compose down -v
```

### API Usage

#### Verify an email:

```bash
http://localhost:5000/api/verify?email=hi@obydul.me
```

Response:

```json
{
  "success": true,
  "send_from": "noreply@shouts.dev",
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
from=EMAIL_ADDESS
email=EMAIL_ADDESS

# example
http://localhost:5000/api/verify?from=noreply@shouts.dev&email=hi@obydul.me
```

### License

This project is licensed under the terms of the MIT license.