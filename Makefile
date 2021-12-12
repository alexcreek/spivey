.PHONY: test

test:
	mkdir -p reports/
	pytest --cov=tdoptions --junitxml=reports/pytest.xml || true
	pylint --exit-zero --disable=R,C --output-format=parseable --reports=y ./tdoptions > reports/pylint.log
