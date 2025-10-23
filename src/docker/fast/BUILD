# Copyright 2022 Pants project contributors.
# Licensed under the Apache License, Version 2.0 (see LICENSE).

docker_image(
    name="my-fast-app",
    # cache_to={"type": "gha", "mode": "max"},
    # cache_from={"type": "gha"},
    source="Dockerfile.python",
    extra_build_args=["DYNAMIC_TAG"],
    image_tags=["0.1-{build_args.DYNAMIC_TAG}"],
)

