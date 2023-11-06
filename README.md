# hairgap-binaries

Provide compiled binaries of [hairgap](https://github.com/cea-sec/hairgap) under the form of a Python package.

## use

```bash
python3 -m pip install hairgap-binaries
```

`hairgap-binaries` only provides `get_hairgapr` and `get_hairgaps` functions that return absolute paths of `hairgapr` and `hairgaps`.
If there are not available for your architecture (e.g., anything else than Linux x86_64), `None` is returned. 

```python
import os

from hairgap_binaries import get_hairgapr, get_hairgaps

assert os.path.isfile(get_hairgapr())
assert os.path.isfile(get_hairgaps())

```

## building 

Requirements:
* python3 (>= 3.5),
* wheel Python package (in the current virtualenv) for creating the .whl package,
* vagrant with the scp plugin.

```bash
tox -e py
```
