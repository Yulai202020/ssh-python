python3 -m build --sdist .
python3 -m build --wheel .

python3 -m twine upload dist/*