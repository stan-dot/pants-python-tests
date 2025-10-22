# Copyright 2022 Pants project contributors.
# Licensed under the Apache License, Version 2.0 (see LICENSE).
#

#  - //:reqs#fastapi
python_requirements(name="reqs")


python_sources(
    name="fast",
)

pex_binary(
    name="main",
    entry_point="main.py",
    dependencies=[":reqs", "src/python/mylib:mylib"],
)
