package io.opentelemetry.instrumentation.api.semconv;

class FooAttributes {
  /**
  * short description of attr_one
  */
  public static final AttributeKey<Boolean> FOO_ATTR_ONE = booleanKey("foo.attr_one");

  /**
  * short description of foo.attr_two
  */
  public static final AttributeKey<String> FOO_ATTR_TWO = stringKey("foo.attr_two");
}