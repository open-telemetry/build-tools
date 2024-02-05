
package io.opentelemetry.instrumentation.api.attributetemplates;

class AttributesTemplate {

  /**
  * this is the description of the first attribute template
  */
  public static final AttributeKey<String> ATTRIBUTE_TEMPLATE_ONE = stringKey("attribute_template_one");

  /**
  * this is the description of the second attribute template. It's a number.
  */
  public static final AttributeKey<Long> ATTRIBUTE_TEMPLATE_TWO = longKey("attribute_template_two");

  /**
  * this is the description of the third attribute template. It's a boolean.
  */
  public static final AttributeKey<Boolean> ATTRIBUTE_THREE = booleanKey("attribute_three");

  /**
  * The name of the client that reported the exception.
  */
  public static final AttributeKey<String> CLIENT_NAME = stringKey("client.name");
}