package io.opentelemetry.instrumentation.api.metric;

class Metrics {

    /**
     * Measures the duration of inbound HTTP requests
     *
     * Instrument: histogram
     * Unit: s
     */
    public static final String HTTP_SERVER_REQUEST_DURATION = "http.server.request.duration";

    /**
     * Measures the number of concurrent HTTP requests that are currently in-flight
     *
     * Instrument: updowncounter
     * Unit: {request}
     */
    public static final String HTTP_SERVER_ACTIVE_REQUESTS = "http.server.active_requests";

    /**
     * Measures the size of HTTP request messages
     *
     * Instrument: histogram
     * Unit: By
     */
    public static final String HTTP_SERVER_REQUEST_BODY_SIZE = "http.server.request.body.size";

}