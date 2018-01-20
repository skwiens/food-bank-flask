export DEBUG=True
export OAUTHLIB_INSECURE_TRANSPORT=1
export SECRET_KEY='clavesecreto'
export ADMIN_EMAIL='xana.wines.ada@gmail.com'
export DATABASE_URL="sqlite:///$(pwd)/app.db"
export CLIENT_SECRET='_kEtgRvZDc5oIqujt_Qle9FL'
echo $DATABASE_URL

python flask-app.py
