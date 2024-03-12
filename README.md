https://medium.com/@rahulxsharma/django-on-google-cloud-run-3f2f93ae0917

1. Download google cloud cli

2. Create a service account

3. update .env file & docker-compose.yml

PYTHON_ENV=dev
PORT=8000
SECRET_KEY=<SECRET>
GS_BUCKET_NAME=lionlifegame

USE_CLOUD_SQL_AUTH_PROXY=True
GOOGLE_CLOUD_PROJECT=peaceful-joy-378401

DATABASE_URL=postgres://postgres:postgres@//cloudsql/peaceful-joy-378401:asia-east1:lifegame/lifegame

GOOGLE_APPLICATION_CREDENTIALS=/secrets/creds.json

4. enable cloud build service 

5. create secrets
gcloud secrets create django_app_settings --replication-policy automatic
gcloud secrets versions add django_app_settings --data-file .env.prod

# Get the PROJECTNUM from your GCP project dashboard
gcloud secrets add-iam-policy-binding django_app_settings --member serviceAccount:342607320219@cloudbuild.gserviceaccount.com --role roles/secretmanager.secretAccessor

gcloud secrets describe django_app_settings



gcloud secrets create django_app_settings --replication-policy automatic
gcloud secrets versions add django_app_settings --data-file .env.prod

# Get the PROJECTNUM from your GCP project dashboard
gcloud secrets add-iam-policy-binding django_app_settings --member serviceAccount:coetics@level-elevator-416109.iam.gserviceaccount.com --role roles/secretmanager.secretAccessor
gcloud secrets describe django_app_settings

6. 

### LOCAL
$env:GOOGLE_APPLICATION_CREDENTIALS="C:\Users\wanyi\git\lifegame_portal\creds.json"

### jupyter notebook
python manage.py shell_plus --notebook