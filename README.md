# Simple FastAPI App

Small example FastAPI application with tests.

Files created:
- `app/main.py` — FastAPI application
- `app/schemas.py` — pydantic models
- `tests/test_main.py` — pytest tests using TestClient
- `requirements.txt` — dependencies

Quick start (Windows PowerShell):

```powershell
# create virtualenv (optional)
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# install dependencies
python -m pip install -r requirements.txt

# run tests
python -m pytest -q

# run server
uvicorn app.main:app --reload
```

GitOps / ArgoCD notes
---------------------

This repository includes a `manifests/` directory with a kustomize base and two overlays:

- `manifests/overlays/dev` — used for development (branch `dev`)
- `manifests/overlays/prod` — used for production (branch `main`)

An Actions workflow `/.github/workflows/gitops.yml` runs on pushes to `dev` and `main`. It:

1. Builds and pushes a container image to the external registry (value taken from the `REGISTRY` secret).
2. Writes the overlay `patch-deployment.yaml` for the branch (dev or prod) to point the deployment at the new `image:tag`.
3. Commits and pushes the overlay change back to this repo — ArgoCD should be configured to watch the `manifests/overlays/<env>` path and will sync the new revision automatically.

Required repository secrets for the workflow (set in Settings → Secrets → Actions):

- `REGISTRY` — Docker registry host (example: `docker.io` or `registry.example.com`)
- `DOCKER_USERNAME` — Registry username
- `DOCKER_PASSWORD` — Registry password or token

Notes:
- The `gitops` workflow uses the branch name to decide the target overlay: `dev` -> `manifests/overlays/dev`, `main` -> `manifests/overlays/prod`.
- For Docker Hub, ensure the registry image path matches your Docker Hub namespace, or change `IMAGE_NAME` usage in the workflow to use a `REMOTE_REPOSITORY` secret if the registry namespace differs from the GitHub repo owner.

Versioning & production deployment
---------------------------------

- The workflows are now tag-aware. When you push a git tag (for example `v1.2.3`), the CI will build an image tagged with the git tag and the GitOps workflow will update the `prod` overlay to use that tagged image. This ensures production manifests are only updated when you create a tag.
- Development builds (branch `dev`) use the commit SHA as the image tag and update the `dev` overlay.
- Required behavior:
	- Create a tag (e.g. `git tag v1.2.3 && git push origin v1.2.3`) to promote to production.
	- Push to `dev` to deploy to the development overlay.

