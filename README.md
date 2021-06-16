# Yardsale Manager API

A Flask-Based Backend/API for the Yardsale Manager App [yardsalemanager.com](https://yardsalemanager.com)

This backend handles user authentication, using JWTs, and handles emailing user confirmation, and password reset emails.

## Local development

You'll need to create a `.env` file with the following contents (replacing the appropriate values)
```bash
export ENVIRONMENT=dev
export SERVER_HOST=localhost
export SERVER_PORT=8000
export HOST_BASE_URL=http://127.0.0.1:8000
export CLIENT_BASE_URL=http://localhost:3000
export SECRET_KEY=<Your secret key here>
export SEND_GRID_API_KEY=<Your SendGrid API key here>
export SEND_GRID_FROM_EMAIL=support@yourdomain.com
export SEND_GRID_TO_EMAIL=user@yourdomain.com
export BCRYPT_SALT=<Your bcrypt salt here>
export GRAPHQL_ENDPOINT=http://localhost:8080/v1/graphql
export GRAPHQL_ADMIN_SECRET="Hasura graphql admin secret here"
```

Run `source .env` to apply the environment variables

Next, you'll want to set up a python virtual environment by running `python3 -m venv venv` and activate it with `source ./venv/bin/activate` (assuming not on Windows).

Install the dependencies with `pip install -r requirements.txt`

Run the server by running `python server.py`

## Notes

There is a docker container running a postgres database with a Hasura graphql layer exposed at `GRAPHQL_ENDPOINT`

TODO: Add documentation to set up the database, and set up Hasura migrations for local, staging, and production.
