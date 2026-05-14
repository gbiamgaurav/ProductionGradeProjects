
## Helper Commands 

gcloud auth login

gcloud auth application-default login

gcloud config set project enterpriserag-496016

gcloud projects describe EnterpriseRAG --format="value(projectNumber)"

gcloud auth list 

gcloud config list

gcloud projects list

gcloud config set project enterpriserag-496016

gcloud auth application-default set-quota-project enterpriserag-496016

gcloud beta billing projects describe enterpriserag-496016

gcloud services enable \
    artifactregistry.googleapis.com \
    run.googleapis.com \
    cloudbuild.googleapis.com \
    sqladmin.googleapis.com \
    documentai.googleapis.com \
    compute.googleapis.com \
    discoveryengine.googleapis.com

