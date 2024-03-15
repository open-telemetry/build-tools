package io.opentelemetry.instrumentation.api.semconv;

class FirstAttributes {
  /**
  * short description of attr_one_a
  */
  public static final AttributeKey<Long> FIRST_ATTR_ONE_A = longKey("first.attr_one_a");

  /**
  * this is the description of attribute template
  */
  public static final AttributeKeyTemplate<String> FIRST_ATTR_TEMPLATE_ONE = stringKey("first.attr_template_one");

  /**
  * short description of last_attr
  */
  public static final AttributeKey<Boolean> FIRST_LAST_ATTR = booleanKey("first.last_attr");
}