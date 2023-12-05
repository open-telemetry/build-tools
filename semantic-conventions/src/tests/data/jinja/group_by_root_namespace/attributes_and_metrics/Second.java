package io.opentelemetry.instrumentation.api.semconv;

class Second {
  /**
  * short description of attr_two
  */
  public static final AttributeKey<Long> SECOND_ATTR_TWO = longKey("second.attr_two");
  /**
  * second metric description
  *
  * Instrument: histogram
  * Unit: s
  */
  public static final String SECOND_METRIC_NAME = "second.metric.name";
}