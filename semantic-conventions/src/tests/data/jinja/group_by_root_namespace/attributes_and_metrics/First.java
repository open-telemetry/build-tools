package io.opentelemetry.instrumentation.api.semconv;

class First {
  /**
  * short description of attr_one
  */
  public static final AttributeKey<Boolean> FIRST_ATTR_ONE = booleanKey("first.attr_one");
  /**
  * first metric description
  *
  * Instrument: counter
  * Unit: {one}
  */
  public static final String FIRST_METRIC_NAME = "first.metric.name";
}