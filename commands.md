

Full local build
```python
pip3 install . -v
```

Editable build for testing

1. Remove_skbuild
2. ```python
pip3 install -v --no-build-isolation --editable .
```

Test

```python
pytest '/Users/Shared/Work/spreader.py/code/wrappers/python'
```

Make source distribution

```python
rm -rf code/wrappers/python/src/spreader.egg-info
mkdir -p dist/tmp
python setup.py egg_info --egg-base dist/tmp sdist 
```

Make wheel

```python
rm -rf code/wrappers/python/src/spreader.egg-info
mkdir -p dist/tmp
python setup.py egg_info --egg-base dist/tmp bdist_wheel 
```


