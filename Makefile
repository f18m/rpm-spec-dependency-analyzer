dist:
	python3 setup.py sdist
	python3 setup.py bdist_wheel

clean:
	rm -rf build dist python_rpm_spec_dependency_analyzer.egg-info rpm_spec_dependency_analyzer.egg-info

test_install:
	sudo pip3 uninstall rpm-spec-dependency-analyzer
	sudo pip3 install dist/rpm_spec_dependency_analyzer-*.whl
	@echo
	@echo "Running installed utility:"
	@echo
	rpm_spec_dependency_analyzer --help

upload:
	twine upload dist/*

.PHONY: dist clean test_install upload
