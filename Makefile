.PHONY: test

test:
	mkdir -p reports/
	pytest --cov=package --junitxml=reports/pytest.xml || true
	pylint --exit-zero --disable=R,C --output-format=parseable --reports=y ./package > reports/pylint.log
