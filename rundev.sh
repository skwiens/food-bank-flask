export DEBUG=True
export OAUTHLIB_INSECURE_TRANSPORT=1
export SECRET_KEY='clavesecreto'
# export CLIENT_SECRET_FILE='client_secret.json'
# export CLIENT_SECRETS_FILE='{"web":{"client_id":"673297702802-r4d8gnq8hamha90la46ghjeodakadd83.apps.googleusercontent.com","project_id":"bethany-food-bank","auth_uri":"https://accounts.google.com/o/oauth2/auth","token_uri":"https://accounts.google.com/o/oauth2/token","auth_provider_x509_cert_url":"https://www.googleapis.com/oauth2/v1/certs","client_secret":"yNkGWUO9oIxjxqbxYlClvJKs","redirect_uris":["https://bethany-food-bank.herokuapp.com/oauth2callback","http://localhost:5000/oauth2callback","http://localhost:8080/oauth2callback","http://localhost:8080/"],"javascript_origins":["https://bethany-food-bank.herokuapp.com","http://localhost:5000"]}}'
export CLIENT_ID='673297702802-r4d8gnq8hamha90la46ghjeodakadd83.apps.googleusercontent.com'
export ADMIN_EMAIL='xana.wines.ada@gmail.com'
export DATABASE_URL="sqlite:///$(pwd)/app.db"
export CLIENT_SECRET='yNkGWUO9oIxjxqbxYlClvJKs'
echo $DATABASE_URL

python flask-app.py
# python
