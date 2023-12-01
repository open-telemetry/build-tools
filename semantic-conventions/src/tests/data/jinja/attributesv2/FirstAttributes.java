package io.opentelemetry.instrumentation.api.semconv;

class FirstAttributes {
  /**
  * short description of attr_one
  */
  public static final AttributeKey<Boolean> FIRST_ATTR_ONE = booleanKey("first.attr_one");

  /**
  * short description of attr_one_a
  */
  public static final AttributeKey<Long> FIRST_ATTR_ONE_A = longKey("first.attr_one_a");

  /**
  * this is the description of attribute template
  */
  public static final AttributeKey<String> FIRST_ATTR_TEMPLATE_ONE = stringKey("first.attr_template_one");
}