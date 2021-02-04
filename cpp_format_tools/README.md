# C++ Format Tools + Docker

A lightweight Docker image, published as otel/cpp_format_tools to Docker Hub,
with all dependencies and tools built-in, to format C++ code.

## What's included in the image

- clang-format
- cmake-format
- buildifier

## Usage

```bash
docker run --rm --privileged=true --volume ${PWD}:/otel otel/cpp_format_tools
```
