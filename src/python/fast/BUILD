# Copyright 2022 Pants project contributors.
# Licensed under the Apache License, Version 2.0 (see LICENSE).
#



python_sources(
    name="fast",
)

pex_binary(
    name="main",
    entry_point="main.py",
    dependencies=[
        ":reqs",
        "src/python/third_party:shared-dependencies",
        "src/python/third_party:api-dependencies",
        "src/python/mylib:mylib"
     ],
)
