https://cloud.google.com/python/django/run#gcloud_4
- Enable cloud build service: https://cloud.google.com/build/docs/securing-builds/configure-access-for-cloud-build-service-account

gcloud builds submit --config cloudmigrate.yaml \
    --substitutions _INSTANCE_NAME=portal,_REGION=asia-east2

gcloud run deploy portal \
    --platform managed \
    --region asia-east2 \
    --image gcr.io/elated-strength-367005/portal \
    --add-cloudsql-instances elated-strength-367005:asia-east2:portal \
    --allow-unauthenticated