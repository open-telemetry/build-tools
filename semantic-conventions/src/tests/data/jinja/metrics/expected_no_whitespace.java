package io.opentelemetry.instrumentation.api.metric;

class Units {
    /**
    * Use this unit for Metric Instruments recording values
    * representing fraction of a total.
    **/
    public static final String PERCENT = "%";
    /**
    * Use this unit for Metric Instruments recording values
    * representing time.
    **/
    public static final String NANOSECOND = "NS";
    /**
    * Use this unit for Metric Instruments recording values
    * representing connections.
    **/
    public static final String CONNECTIONS = "{connections}";
}