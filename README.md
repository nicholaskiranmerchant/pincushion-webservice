# SDQ
## Open TODOs:
### High-priority
- [ ] Host the application on Kubernetes
- [ ] List the application on the public internet
- [ ] Set up GitLab CI/CD
- [ ] Create NoSQL post/list functionality
### Low-priority
- [ ] Correctly configure pyproject.toml

## Testing & Deploying
0. Navigate to the project root directory
1. Activate the venv with `source venv/bin/activate`
2. Run unit tests with `pytest sdq`
3. Debug the flask app locally with `flask --app sdq/src/wsgi:app --debug run`
4. Rebuild the docker container using `docker build -t sdq .`
5. Test the docker container with `docker run -p 80:80 --name sdq sdq:latest`
6. Push the docker container to GKE with 
docker tag sdq us-east1-docker.pkg.dev/sdq1-382716/sdq/sdq:<new-tag-name>
docker push us-east1-docker.pkg.dev/sdq1-382716/sdq/sdq:<new-tag-name>

kubectl set image deployment/sdq-gke-deployment sdq=us-east1-docker.pkg.dev/sdq1-382716/sdq/sdq:<new-tag-name>