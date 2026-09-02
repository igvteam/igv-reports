**Run the tests**

```bash
python3 -m unittest discover -s test -t .
```

**Bump version number in pyproject.toml**

This is the only place the version is set. `igv_reports.__version__` and the `--version` flag of
`create_report` and `create_datauri` read it from the installed package metadata.

**Add git version tag**

The tag must point at a commit that is already on the remote, so push the branch first.

```bash
git push origin master
git tag vX.Y.Z
git push origin vX.Y.Z
```

**Clean previous build artifacts**

```bash
rm -rf build dist igv_reports.egg-info
```

Do not skip this. setuptools uses `build/` as a scratch directory and does not remove files that
are no longer in the source, so a stale `build/` can put deleted modules into the wheel. A stale
`build/` directory also shadows the `build` module itself, making `python3 -m build` fail with
"'build' is a package and cannot be directly executed". A stale `igv_reports.egg-info` makes
`create_report --version` report the previous version when run from a source checkout.

**Build the archive**

Requires the build package (`pip install build`).

```bash
python3 -m build
```

**Upload to test.pypi**

```bash
python -m twine upload --repository-url https://test.pypi.org/legacy/ dist/*
```

**Install from test.pypi and check the version**

```bash
pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple igv-reports
create_report --version
```

Make sure the version is the one you just uploaded.

**Upload to pypi**

```bash
python -m twine upload dist/*
```

**Publish the release notes**

Create a GitHub release against the tag and describe what changed, calling out anything that
alters the output of an existing report.
