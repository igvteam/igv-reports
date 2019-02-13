

**Bump version number**

**Add version tag**

**Build the archive**

```bash
python setup.py sdist bdist_wheel
```

**Upload to test.pypi**

```bash
python -m twine upload --repository-url https://test.pypi.org/legacy/ dist/*
```

**Upload to pypi**

```bash
python twine upload
```


**Installing from test.pypi**

pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple igv-reports
