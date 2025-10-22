# Copyright 2022 Pants project contributors.
# Licensed under the Apache License, Version 2.0 (see LICENSE).

python_sources(
    name="mylib",
)




python_distribution(
    name="dist",
    dependencies=[":lib"],
    wheel=True,
    sdist=True,
    provides=setup_py(
        name="mylib",
        version="0.0.1",
        description="A Python library for testing.",
    ),
)

