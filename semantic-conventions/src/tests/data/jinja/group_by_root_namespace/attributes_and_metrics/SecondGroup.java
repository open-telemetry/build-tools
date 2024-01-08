package io.opentelemetry.instrumentation.api.semconv;

import io.opentelemetry.api.metrics.Meter;

class SecondGroup {
  /**
  * short description of attr_two
  */
  public static final AttributeKey<Long> SECOND_GROUP_ATTR_TWO = longKey("second_group.attr_two");
  /**
  * second metric description
  * Experimental: True
  */
  public static final DoubleHistogramBuilder createSecondGroupMetric(Meter meter) {
    return meter.histogramBuilder("second_group.metric")
            .setDescription("second metric description")
            .setUnit("s");
  }
}