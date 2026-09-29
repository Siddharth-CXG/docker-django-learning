# HTTP Contracts: Energy Dashboard

All routes are served by the Django application. HTML pages use normal browser navigation; the health route returns JSON. No third-party API is involved.

## Page routes

| Method | Path | Response |
|---|---|---|
| GET | `/` | Home page with title, introduction, and three placeholder statistics |
| GET | `/assets/` | Page containing exactly four example assets with name, type, and status |
| GET | `/about/` | Educational purpose and Docker containerisation explanation |
| GET | `/contact/` | Contact form with name, email, and message fields |

The shared navigation links to Home, Assets, About, and Contact. Page responses use responsive HTML and plain CSS.

## Contact submission

| Method | Path | Request | Response |
|---|---|---|---|
| POST | `/contact/` | Standard form fields `name`, `email`, and `message`, with CSRF protection | Invalid submissions re-render the form with field errors and submitted values; valid submissions are saved locally and show an on-page confirmation without sending email |

All three fields are required. Email must be valid. Whitespace-only values are invalid. Valid submissions are saved once per accepted POST; no public listing or edit/delete interface is included.

## Health check

| Method | Path | Response |
|---|---|---|
| GET | `/health/` | HTTP 200, `Content-Type: application/json`, body `{"status":"healthy"}` |

The health response confirms application request handling only; it does not claim to validate database health.

## Local access

The container listens on port 8000 at `0.0.0.0`. Publishing the port with Docker host mapping `8000:8000` makes the pages available at `http://localhost:8000`. `EXPOSE 8000` is image metadata and does not publish the host port by itself.