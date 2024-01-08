package io.opentelemetry.instrumentation.api.semconv;

import io.opentelemetry.api.metrics.Meter;

class First {
  /**
  * short description of attr_one
  */
  public static final AttributeKey<Boolean> FIRST_ATTR_ONE = booleanKey("first.attr_one");
  /**
  * first metric description
  * Experimental: False
  */
  public static final LongCounterBuilder createFirstMetric(Meter meter) {
    return meter.counterBuilder("first.metric")
            .setDescription("first metric description")
            .setUnit("{one}");
  }
}