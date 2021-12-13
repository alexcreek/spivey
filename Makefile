.PHONY: test

test:
	mkdir -p reports/
	pytest --cov=spivey --junitxml=reports/pytest.xml || true
	pylint --exit-zero --disable=R,C --output-format=parseable --reports=y ./spivey > reports/pylint.log
