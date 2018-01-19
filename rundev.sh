export DEBUG=True
export OAUTHLIB_INSECURE_TRANSPORT=1
export SECRET_KEY='clavesecreto'
# export CLIENT_SECRET_FILE='client_secret.json'
export CLIENT_SECRET_FILE={"web":{"client_id":"673297702802-meoqb93la7chfs2frqpbqrdqa0c0ts0k.apps.googleusercontent.com","project_id":"bethany-food-bank","auth_uri":"https://accounts.google.com/o/oauth2/auth","token_uri":"https://accounts.google.com/o/oauth2/token","auth_provider_x509_cert_url":"https://www.googleapis.com/oauth2/v1/certs","client_secret":"_kEtgRvZDc5oIqujt_Qle9FL","redirect_uris":["https://bethany-food-bank.herokuapp.com/oauth2callback","http://localhost:5000/oauth2callback"],"javascript_origins":["https://bethany-food-bank-heroku.herokuapp.com","http://localhost:5000"]}}
export CLIENT_ID='673297702802-meoqb93la7chfs2frqpbqrdqa0c0ts0k.apps.googleusercontent.com'
export ADMIN_EMAIL='xana.wines.ada@gmail.com'
export DATABASE_URL="sqlite:///$(pwd)/app.db"
export CLIENT_SECRET='_kEtgRvZDc5oIqujt_Qle9FL'
echo $DATABASE_URL

python flask-app.py
