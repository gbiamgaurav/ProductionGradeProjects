
gcloud projects add-iam-policy-binding enterpriserag-496016 \
    --member="user:codebygaurav29@gmail.com" \
    --role="roles/run.admin"

gcloud projects add-iam-policy-binding enterpriserag-496016 \
    --member="user:codebygaurav29@gmail.com" \
    --role="roles/artifactregistry.admin" 

gcloud projects add-iam-policy-binding enterpriserag-496016 \
    --member="user:codebygaurav29@gmail.com" \
    --role="roles/storage.admin"

gcloud projects add-iam-policy-binding enterpriserag-496016 \
    --member="user:codebygaurav29@gmail.com" \
    --role="roles/cloudsql.client"


gcloud projects add-iam-policy-binding enterpriserag-496016 \
    --member="user:codebygaurav29@gmail.com" \
    --role="roles/aiplatform.user"


gcloud projects add-iam-policy-binding enterpriserag-496016 \
    --member="user:codebygaurav29@gmail.com" \
    --role="roles/documentai.apiUser"


gcloud projects add-iam-policy-binding enterpriserag-496016 \
    --member="user:codebygaurav29@gmail.com" \
    --role="roles/discoveryengine.editor"


## Grant Document AI access to the Cloud Run Service Account
gcloud projects add-iam-policy-binding enterpriserag-496016 \
    --member="serviceAccount:726456204117-compute@developer.gserviceaccount.com" \
    --role="roles/documentai.apiUser"


# Grand VPC access to the Cloud Run Service Agent
gcloud projects add-iam-policy-binding enterpriserag-496016 \
--member="serviceAccount:service-726456204117@serverless-robot-prod.iam.gserviceaccount.com" \
--role="roles/vpcaccess.user"

# Grant permission to the Cloud Run Service Account (Production)
gcloud projects add-iam-policy-binding enterpriserag-496016 \
--member="serviceAccount:726456204117-compute@developer.gserviceaccount.com" \
--role="roles/discoveryengine.editor"