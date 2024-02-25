# E2E Tests for Django/Svelte

This is an absolutely minimal app which demonstrates how you can integrate
Svelte and Django together in order to produce end-to-end tests driven from the
Django side but which encapsulate the whole application.

## Installation

For this project we are going to use [bun](https://bun.sh/) as a JS runtime and
[uv](https://github.com/astral-sh/uv) as a Python package manager, because they
are so much faster and so easy to install. Still the procedure would work with
`pip`, `node` and `npm` if you'd like so feel free to translate. We also assume
that you have `make` installed in a Linux/Mac-ish shell.

```bash
bash -c 'cd front && bun install'
bash -c 'cd api && make sync'
```

Then you got to make sure to install the Playwright browsers:

```bash
bash -c 'cd api && make playwright'
```

## Running the tests

You can run the tests from the `api` folder using `pytest`. Which his done with
the following shortcut:

```bash
cd api
make test
```
