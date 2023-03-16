# Copyright 2019 The Kubernetes Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
SHELL := /bin/bash

# Install dependencies
.PHONY: install
install:
	# Create python virtual environment
	python3 -m venv venv/

	# Active virtual environment
	source ./venv/bin/activate

	# Install python depdendencies
	pip install -r requirements.txt


# Build the documentation.
.PHONY: docs
docs:
	# Ensure site dir exists
	mkdir -p site

	# Generate docs with mkdocs
	mkdocs build


# Cleanup local directory
.PHONY: cleanup
cleanup:
	# Remove python virtual environment
	rm -rf venv

	# Remove site build
	rm -rf site
