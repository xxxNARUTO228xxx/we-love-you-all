echo "##### Flake8: ##### \n"
flake8 .

echo "##### MyPy: ##### \n"
mypy .

echo "##### Bandit: ##### \n"
bandit --ini setup.cfg -r .

echo "##### Pycodestyle: ##### \n"
pycodestyle .

echo "##### Pydoctyle: ##### \n"
pydocstyle .
