import kagglehub

# Download latest version
path = kagglehub.dataset_download("yoadjei/adversarial-bec-email-dataset")

print("Path to dataset files:", path)