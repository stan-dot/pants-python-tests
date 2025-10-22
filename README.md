# pants-python-tests

<https://www.pantsbuild.org/stable/docs/getting-started/incremental-adoption#4-set-up-pants-package>
to setup the tests one needs

- source roots setup <https://www.pantsbuild.org/stable/docs/using-pants/key-concepts/source-roots>
- third party dependency setup <https://www.pantsbuild.org/stable/docs/python/overview/third-party-dependencies>

## questions

1. which is the more pants-idiomatic way of setting up tests? I'd prefer in the same folder ('src/python/fast' would contain `test_*.py files, flat OR in a folder)
2. what is the idiomatic way of running the tests? are they just another target? `pants run target` or `pants test file`?
3. how to run all the tests in the folder? a) `pants run [glob expression] for many files` (with what syntax?) b) per-test mention in `BUILD`?
4. do I need to setup 3rd party dependencies as a separate subproject? <https://www.pantsbuild.org/stable/docs/python/overview/third-party-dependencies> My impression at the moment is that if I like to have tests, their dependencies need to be in that root 3rdparty folder, while regular packages can have `pyproject.toml` or `requirements.txt`, is this correct? Ideally I'd like to declare test dependencies in its own `pyproject.toml` if a separate `package_test` package, OR if in the same package folder, with `pyproject.toml` decorator field as optional dependencies.
5. crucially the use case is for a test package that runs in CI and can instantiate objects from the main package - like FastAPI `app` and use it with an `httpx` client.
