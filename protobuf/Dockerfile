# gRPC core version that applies to C++, C#, Objective-C, PhP, Python, Ruby
# renovate: datasource=github-releases depName=grpc/grpc
ARG GRPC_VERSION=1.82.1
ARG GRPC_COMMIT_SHA=acccf84c0df20487d64101f528e5d426541ca4e5

# renovate: datasource=github-releases depName=protobuf-c/protobuf-c
ARG PROTOBUF_C_VERSION=1.5.2
ARG PROTOBUF_C_SHA256=e2c86271873a79c92b58fef7ebf8de1aa0df4738347a8bd5d4e65a80a16d0d24

# renovate: datasource=github-releases depName=grpc/grpc-web
ARG GRPC_WEB_VERSION=2.0.2
ARG GRPC_WEB_SHA256=0f0c8c0c1104306d67dad678be7c14efe52a698795a58b2b72ab67a8bb100c15

# renovate: datasource=github-releases depName=protocolbuffers/protobuf-go
ARG PROTOC_GEN_GO_VERSION=v1.36.11
ARG PROTOC_GEN_GO_SHA256=517b935001f3d43640489cd1aab531a3ed5927fb34379fa6cb1c1a514e9cb8e8

# renovate: datasource=github-releases depName=grpc/grpc-go
ARG PROTOC_GEN_GO_GRPC_VERSION=v1.5.1
ARG PROTOC_GEN_GO_GRPC_SHA256=54cb438abe590c9366e08251f811810fa004b1193154fe6e6a7d7c782a37332e

# renovate: datasource=github-releases depName=grpc/grpc-java
ARG GRPC_JAVA_VERSION=1.82.2
ARG GRPC_JAVA_SHA256=a8aa94f9df771ff5428f5cf8a5dc0fcd2ebb8fda85b29db84a4c7d8ca2153d5a

# v1.3.2, using the version directly does not work: "tar: invalid magic"
ARG PROTOC_GEN_GOGO_VERSION=b03c65ea87cdc3521ede29f62fe3ce239267c1bc
ARG PROTOC_GEN_GOGO_SHA256=b46e8dc8d5a62d404e1a4aaa3ab6f1781fe67beb663a996281c9c10cc0c4703d

# renovate: datasource=github-releases depName=ckaznocha/protoc-gen-lint
ARG PROTOC_GEN_LINT_VERSION=0.3.0
ARG PROTOC_GEN_LINT_AMD64_SHA256=fc501dff3d478994e0c7b540466ffd365e4fd7401d2d207de6cfb0a7e80d3337
ARG PROTOC_GEN_LINT_ARM64_SHA256=2707dd516902071a1b70fc136382407f76f88ffe960707dac08a5e33312c2f09

# renovate: datasource=github-releases depName=grpc-ecosystem/grpc-gateway
ARG GRPC_GATEWAY_VERSION=v2.29.0
ARG GRPC_GATEWAY_SHA256=c067650666440981109965953c4636cb08a556d0986ad4861167fec4553d8d74

# renovate: datasource=github-releases depName=upx/upx
ARG UPX_VERSION=5.2.0
ARG UPX_AMD64_SHA256=3db5d3294707439db97866feab8d75d800f028f48481a40547411824da4288a1
ARG UPX_ARM64_SHA256=55d48a61e8ffd17152db871c855376cba7f08e830b37799d0947a16dff8ec36c

ARG TARGETARCH=amd64

FROM alpine:3.24@sha256:28bd5fe8b56d1bd048e5babf5b10710ebe0bae67db86916198a6eec434943f8b AS protoc_builder
RUN apk add --no-cache build-base curl automake autoconf libtool git zlib-dev linux-headers cmake ninja pkgconf abseil-cpp-dev patch

RUN mkdir -p /out

ARG GRPC_VERSION
ARG GRPC_COMMIT_SHA
RUN git clone --recursive --depth=1 -b v${GRPC_VERSION} https://github.com/grpc/grpc.git /grpc && \
    test "$(git -C /grpc rev-parse HEAD)" = "${GRPC_COMMIT_SHA}" && \
    ln -s /grpc/third_party/protobuf /protobuf && \
    mkdir -p /grpc/cmake/build && \
    cd /grpc/cmake/build && \
    cmake \
    -GNinja \
    -DBUILD_SHARED_LIBS=ON \
    -DCMAKE_INSTALL_PREFIX=/usr \
    -DCMAKE_BUILD_TYPE=Release \
    -DgRPC_INSTALL=ON \
    -DgRPC_BUILD_TESTS=OFF \
    -DRE2_BUILD_TESTING=OFF \
    -DCMAKE_CXX_STANDARD=17 \
    -DCMAKE_CXX_FLAGS="-include cstdint" \
    ../.. && \
    cmake --build . --target plugins && \
    cmake --build . --target install && \
    DESTDIR=/out cmake --build . --target install

COPY protobuf-c-pr797.patch /tmp/protobuf-c-pr797.patch
ARG PROTOBUF_C_VERSION
ARG PROTOBUF_C_SHA256
RUN mkdir -p /protobuf-c && \
    curl -sSL https://github.com/protobuf-c/protobuf-c/releases/download/v${PROTOBUF_C_VERSION}/protobuf-c-${PROTOBUF_C_VERSION}.tar.gz -o /tmp/protobuf-c.tar.gz && \
    echo "${PROTOBUF_C_SHA256}  /tmp/protobuf-c.tar.gz" | sha256sum -c - && \
    tar xzf /tmp/protobuf-c.tar.gz --strip 1 -C /protobuf-c && \
    rm /tmp/protobuf-c.tar.gz && \
    cd /protobuf-c && \
    # We need to patch a few helper functions to deal with Alpine linux's `absl` library
    # and inability to handle string_view -> string conversions.
    patch -p1 < /tmp/protobuf-c-pr797.patch && \
    rm /tmp/protobuf-c-pr797.patch && \
    export LD_LIBRARY_PATH=/usr/lib:/usr/lib64 && \
    export PKG_CONFIG_PATH=/usr/lib64/pkgconfig:/usr/lib/pkgconfig && \
    ./configure --prefix=/usr && \
    make && make install DESTDIR=/out

ARG GRPC_JAVA_VERSION
ARG GRPC_JAVA_SHA256
RUN mkdir -p /grpc-java && \
    curl -sSL https://github.com/grpc/grpc-java/archive/refs/tags/v${GRPC_JAVA_VERSION}.tar.gz -o /tmp/grpc-java.tar.gz && \
    echo "${GRPC_JAVA_SHA256}  /tmp/grpc-java.tar.gz" | sha256sum -c - && \
    tar xzf /tmp/grpc-java.tar.gz --strip 1 -C /grpc-java && \
    rm /tmp/grpc-java.tar.gz && \
    cd /grpc-java && \
    g++ \
    -I. -I/usr/include \
    compiler/src/java_plugin/cpp/*.cpp \
    -L/usr/lib64 -L/usr/lib \
    -lprotoc -lprotobuf $(pkg-config --libs protobuf) -labsl_raw_hash_set -labsl_log_internal_check_op -labsl_log_internal_message -lpthread --std=c++17 -s \
    -o protoc-gen-grpc-java && \
    install -Ds protoc-gen-grpc-java /out/usr/bin/protoc-gen-grpc-java && \
    rm -Rf /grpc-java && \
    rm -Rf /grpc

COPY grpc-web-protobuf35.patch /tmp/grpc-web-protobuf35.patch
ARG GRPC_WEB_VERSION
ARG GRPC_WEB_SHA256
RUN mkdir -p /grpc-web && \
    curl -sSL https://github.com/grpc/grpc-web/archive/refs/tags/${GRPC_WEB_VERSION}.tar.gz -o /tmp/grpc-web.tar.gz && \
    echo "${GRPC_WEB_SHA256}  /tmp/grpc-web.tar.gz" | sha256sum -c - && \
    tar xzf /tmp/grpc-web.tar.gz --strip 1 -C /grpc-web && \
    rm /tmp/grpc-web.tar.gz && \
    cd /grpc-web && \
    # We need to patch a few helper functions to deal with Alpine linux's `absl` library
    # and inability to handle string_view -> string conversions.
    patch -p1 < /tmp/grpc-web-protobuf35.patch && \
    rm /tmp/grpc-web-protobuf35.patch && \
    make install-plugin CXXFLAGS="-std=c++17 -I/usr/include" LDFLAGS="-L/usr/local/lib -lprotoc -lprotobuf $(pkg-config --libs protobuf) -labsl_log_internal_check_op -labsl_log_internal_message -labsl_raw_hash_set -lpthread -ldl" STATIC=no PREFIX=/out/usr

FROM golang:1.26-alpine@sha256:3889b425f035be855a72fb4755265311293b6d414521f0a519d819df32222d83 AS go_builder
RUN apk add --no-cache build-base curl git

ARG PROTOC_GEN_GO_GRPC_VERSION
ARG PROTOC_GEN_GO_GRPC_SHA256
RUN mkdir -p ${GOPATH}/src/github.com/grpc/grpc-go && \
    curl -sSL https://github.com/grpc/grpc-go/archive/refs/tags/cmd/protoc-gen-go-grpc/${PROTOC_GEN_GO_GRPC_VERSION}.tar.gz -o /tmp/grpc-go.tar.gz && \
    echo "${PROTOC_GEN_GO_GRPC_SHA256}  /tmp/grpc-go.tar.gz" | sha256sum -c - && \
    tar xzf /tmp/grpc-go.tar.gz --strip 1 -C ${GOPATH}/src/github.com/grpc/grpc-go && \
    rm /tmp/grpc-go.tar.gz && \
    cd ${GOPATH}/src/github.com/grpc/grpc-go/cmd/protoc-gen-go-grpc && \
    go build -ldflags '-w -s' -o /golang-protobuf-out/protoc-gen-go-grpc . && \
    install -Ds /golang-protobuf-out/protoc-gen-go-grpc /out/usr/bin/protoc-gen-go-grpc

ARG PROTOC_GEN_GO_VERSION
ARG PROTOC_GEN_GO_SHA256
RUN mkdir -p ${GOPATH}/src/google.golang.org/protobuf && \
    curl -sSL https://github.com/protocolbuffers/protobuf-go/archive/refs/tags/${PROTOC_GEN_GO_VERSION}.tar.gz -o /tmp/protobuf-go.tar.gz && \
    echo "${PROTOC_GEN_GO_SHA256}  /tmp/protobuf-go.tar.gz" | sha256sum -c - && \
    tar xzf /tmp/protobuf-go.tar.gz --strip 1 -C ${GOPATH}/src/google.golang.org/protobuf && \
    rm /tmp/protobuf-go.tar.gz && \
    cd ${GOPATH}/src/google.golang.org/protobuf && \
    go build -ldflags '-w -s' -o /golang-protobuf-out/protoc-gen-go ./cmd/protoc-gen-go && \
    install -Ds /golang-protobuf-out/protoc-gen-go /out/usr/bin/protoc-gen-go

ARG PROTOC_GEN_GOGO_VERSION
ARG PROTOC_GEN_GOGO_SHA256
RUN mkdir -p ${GOPATH}/src/github.com/gogo/protobuf && \
    curl -sSL https://github.com/gogo/protobuf/archive/${PROTOC_GEN_GOGO_VERSION}.tar.gz -o /tmp/gogo.tar.gz && \
    echo "${PROTOC_GEN_GOGO_SHA256}  /tmp/gogo.tar.gz" | sha256sum -c - && \
    tar xzf /tmp/gogo.tar.gz --strip 1 -C ${GOPATH}/src/github.com/gogo/protobuf && \
    rm /tmp/gogo.tar.gz && \
    cd ${GOPATH}/src/github.com/gogo/protobuf && \
    go build -ldflags '-w -s' -o /gogo-protobuf-out/protoc-gen-gofast ./protoc-gen-gofast && \
    install -Ds /gogo-protobuf-out/protoc-gen-gofast /out/usr/bin/protoc-gen-gofast && \
    go build -ldflags '-w -s' -o /gogo-protobuf-out/protoc-gen-gogo ./protoc-gen-gogo && \
    install -Ds /gogo-protobuf-out/protoc-gen-gogo /out/usr/bin/protoc-gen-gogo && \
    go build -ldflags '-w -s' -o /gogo-protobuf-out/protoc-gen-gogofast ./protoc-gen-gogofast && \
    install -Ds /gogo-protobuf-out/protoc-gen-gogofast /out/usr/bin/protoc-gen-gogofast && \
    go build -ldflags '-w -s' -o /gogo-protobuf-out/protoc-gen-gogofaster ./protoc-gen-gogofaster && \
    install -Ds /gogo-protobuf-out/protoc-gen-gogofaster /out/usr/bin/protoc-gen-gogofaster && \
    mkdir -p /out/usr/include/github.com/gogo/protobuf/protobuf/google/protobuf && \
    install -D $(find ./protobuf/google/protobuf -name '*.proto') -t /out/usr/include/github.com/gogo/protobuf/protobuf/google/protobuf && \
    install -D ./gogoproto/gogo.proto /out/usr/include/github.com/gogo/protobuf/gogoproto/gogo.proto

ARG PROTOC_GEN_LINT_VERSION
ARG PROTOC_GEN_LINT_AMD64_SHA256
ARG PROTOC_GEN_LINT_ARM64_SHA256
ARG TARGETARCH
RUN cd / && \
    curl -sSLO https://github.com/ckaznocha/protoc-gen-lint/releases/download/v${PROTOC_GEN_LINT_VERSION}/protoc-gen-lint_linux_${TARGETARCH}.zip && \
    if [ "${TARGETARCH}" = "amd64" ]; then \
        echo "${PROTOC_GEN_LINT_AMD64_SHA256}  protoc-gen-lint_linux_${TARGETARCH}.zip" | sha256sum -c -; \
    else \
        echo "${PROTOC_GEN_LINT_ARM64_SHA256}  protoc-gen-lint_linux_${TARGETARCH}.zip" | sha256sum -c -; \
    fi && \
    mkdir -p /protoc-gen-lint-out && \
    cd /protoc-gen-lint-out && \
    unzip -q /protoc-gen-lint_linux_${TARGETARCH}.zip && \
    install -Ds /protoc-gen-lint-out/protoc-gen-lint /out/usr/bin/protoc-gen-lint

ARG GRPC_GATEWAY_VERSION
ARG GRPC_GATEWAY_SHA256
RUN mkdir -p ${GOPATH}/src/github.com/grpc-ecosystem/grpc-gateway && \
    curl -sSL https://github.com/grpc-ecosystem/grpc-gateway/archive/refs/tags/${GRPC_GATEWAY_VERSION}.tar.gz -o /tmp/grpc-gateway.tar.gz && \
    echo "${GRPC_GATEWAY_SHA256}  /tmp/grpc-gateway.tar.gz" | sha256sum -c - && \
    tar xzf /tmp/grpc-gateway.tar.gz --strip 1 -C ${GOPATH}/src/github.com/grpc-ecosystem/grpc-gateway && \
    rm /tmp/grpc-gateway.tar.gz && \
    cd ${GOPATH}/src/github.com/grpc-ecosystem/grpc-gateway && \
    go build -ldflags '-w -s' -o /grpc-gateway-out/protoc-gen-grpc-gateway ./protoc-gen-grpc-gateway && \
    go build -ldflags '-w -s' -o /grpc-gateway-out/protoc-gen-openapiv2 ./protoc-gen-openapiv2 && \
    install -Ds /grpc-gateway-out/protoc-gen-grpc-gateway /out/usr/bin/protoc-gen-grpc-gateway && \
    install -Ds /grpc-gateway-out/protoc-gen-openapiv2 /out/usr/bin/protoc-gen-openapiv2 && \
    mkdir -p /out/usr/include/protoc-gen-openapiv2/options && \
    install -D $(find ./protoc-gen-openapiv2/options -name '*.proto') -t /out/usr/include/protoc-gen-openapiv2/options

FROM alpine:3.24@sha256:28bd5fe8b56d1bd048e5babf5b10710ebe0bae67db86916198a6eec434943f8b AS packer
RUN apk add --no-cache curl

ARG UPX_VERSION
ARG UPX_AMD64_SHA256
ARG UPX_ARM64_SHA256
ARG TARGETARCH
RUN mkdir -p /upx && \
    curl -sSL https://github.com/upx/upx/releases/download/v${UPX_VERSION}/upx-${UPX_VERSION}-${TARGETARCH}_linux.tar.xz -o /tmp/upx.tar.xz && \
    if [ "${TARGETARCH}" = "amd64" ]; then \
        echo "${UPX_AMD64_SHA256}  /tmp/upx.tar.xz" | sha256sum -c -; \
    else \
        echo "${UPX_ARM64_SHA256}  /tmp/upx.tar.xz" | sha256sum -c -; \
    fi && \
    tar xJ --strip 1 -C /upx -f /tmp/upx.tar.xz && \
    rm /tmp/upx.tar.xz && \
    install -D /upx/upx /usr/local/bin/upx

# Use all output including headers and protoc from protoc_builder
COPY --from=protoc_builder /out/ /out/

# Integrate all output from go_builder
COPY --from=go_builder /out/ /out/

RUN upx --lzma $(find /out/usr/bin/ -type f ! -type l \
    \( -name 'grpc_*' \
    -not -name 'grpc_csharp_plugin' \
    -not -name 'grpc_node_plugin' \
    -not -name 'grpc_php_plugin' \
    -not -name 'grpc_ruby_plugin' \
    -not -name 'grpc_python_plugin' \
    -or -name 'protoc-gen-*' \) ! -type l \
    )
RUN find /out -name "*.a" -delete -or -name "*.la" -delete


FROM alpine:3.24@sha256:28bd5fe8b56d1bd048e5babf5b10710ebe0bae67db86916198a6eec434943f8b
LABEL maintainer="The OpenTelemetry Authors"
COPY --from=packer /out/ /
RUN apk add --no-cache bash libstdc++ && \
    ln -s /usr/bin/grpc_cpp_plugin /usr/bin/protoc-gen-grpc-cpp && \
    ln -s /usr/bin/grpc_csharp_plugin /usr/bin/protoc-gen-grpc-csharp && \
    ln -s /usr/bin/grpc_objective_c_plugin /usr/bin/protoc-gen-grpc-objc && \
    ln -s /usr/bin/grpc_node_plugin /usr/bin/protoc-gen-grpc-js && \
    ln -s /usr/bin/grpc_php_plugin /usr/bin/protoc-gen-grpc-php && \
    ln -s /usr/bin/grpc_python_plugin /usr/bin/protoc-gen-grpc-python && \
    ln -s /usr/bin/grpc_ruby_plugin /usr/bin/protoc-gen-grpc-ruby
COPY protoc-wrapper /usr/bin/protoc-wrapper
ENV LD_LIBRARY_PATH='/usr/lib:/usr/lib64:/usr/lib/local'
ENTRYPOINT ["protoc-wrapper", "-I/usr/include"]
