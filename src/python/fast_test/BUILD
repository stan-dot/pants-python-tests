# Copyright 2020 Pants project contributors.
# Licensed under the Apache License, Version 2.0 (see LICENSE).

# This target sets the metadata for all the Python non-test files in this directory.
#
# * Pants cannot yet infer dependencies on `resource` / `resources` targets, so we explicitly add
#   the dep.
python_sources(
    name="lib",
)


# This target sets the metadata for all the Python test files in this directory.
python_tests(
    name="test",
    dependencies=[
        ":lib",
        "src/python/third_party:shared-dependencies",
        "src/python/third_party:test-dependencies",
        "src/python/fast:main",
    ],
)

python_test_utils(
    name="test_utils",
)
