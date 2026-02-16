# Setting Up PyPI Trusted Publishing

The automated release workflow uses PyPI's [Trusted Publishing](https://docs.pypi.org/trusted-publishers/) feature, which allows GitHub Actions to publish packages without needing to store API tokens as secrets.

## One-Time Setup Required

Before the automated release workflow can publish to PyPI, you need to configure trusted publishing on PyPI:

### Steps:

1. **Go to PyPI**: Visit https://pypi.org/manage/account/publishing/

2. **Add a new publisher** with these details:
   - **PyPI Project Name**: `akeyless-cloud-id`
   - **Owner**: `<your-github-org-or-username>`
   - **Repository name**: `akeyless-python-cloud-id`
   - **Workflow name**: `release.yml`
   - **Environment name**: `pypi`

3. **Save** the publisher configuration

### Alternative: Using API Token (Legacy Method)

If you prefer to use an API token instead of trusted publishing:

1. Generate an API token at https://pypi.org/manage/account/token/
2. Add it as a GitHub secret named `PYPI_API_TOKEN` in your repository settings
3. Modify `.github/workflows/release.yml` to use the token:

```yaml
- name: Publish to PyPI
  uses: pypa/gh-action-pypi-publish@release/v1
  with:
    password: ${{ secrets.PYPI_API_TOKEN }}
```

## Testing with TestPyPI (Recommended)

Before setting up production PyPI publishing, test with TestPyPI:

1. Go to https://test.pypi.org/manage/account/publishing/
2. Set up trusted publishing with the same details
3. Create a test release by pushing a tag like `v0.3.1-test`
4. Modify the workflow temporarily to publish to TestPyPI:

```yaml
- name: Publish to TestPyPI
  uses: pypa/gh-action-pypi-publish@release/v1
  with:
    repository-url: https://test.pypi.org/legacy/
```

## Security Notes

- Trusted publishing is more secure than API tokens because:
  - No long-lived credentials are stored
  - Publishing is tied to specific GitHub repository and workflow
  - PyPI verifies the identity of the publisher using OIDC

- The workflow requires explicit approval for the `pypi` environment
- Only tags matching `v*.*.*` pattern will trigger releases
- Version validation ensures tag matches code version before publishing
