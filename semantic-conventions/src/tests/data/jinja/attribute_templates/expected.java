
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
}