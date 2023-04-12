# SDQ
## Open TODOs:
### High-priority
- [x] Host the application on Kubernetes
- [ ] List the application on a public DNS
- [x] Set up GitLab CI/CD
- [x] Create NoSQL post/list functionality
### Low-priority
- [ ] Correctly configure pyproject.toml

## Testing & Deploying
0. Navigate to the project root directory
1. Activate the venv with `source venv/bin/activate`
2. Run unit tests with `pytest sdq`
3. Debug the flask app locally with `flask --app sdq/src/wsgi:app --debug run`
4. Push the changes to master using
    - `git add -A`
    - `git commit -m "<your message>"`
    - `git push`

5. Update the GKE cluster to the newest image
    - Get all images with: 
        - `gcloud container images list-tags us-east1-docker.pkg.dev/sdq1-382716/sdq/sdq`
    - Verify a recent tag has been created. If there is no recent tag, the GitLab pipelines are still executing.
        - [View status for current and past pipelines](https://gitlab.com/nicholaskiranmerchant_portfolio/sdq/-/pipelines)
    - Copy the new tag name, and run:
        - `kubectl set image deployment/sdq-server sdq=us-east1-docker.pkg.dev/sdq1-382716/sdq/sdq:<new-tag-name>`