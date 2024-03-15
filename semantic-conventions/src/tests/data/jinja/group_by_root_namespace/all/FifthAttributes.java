package io.opentelemetry.instrumentation.api.semconv;

class FifthAttributes {
  /**
  * short description of attr_five_int
  */
  public static final AttributeKey<Enum> FIFTH_ATTR_FIVE_INT = enumKey("fifth.attr_five_int");

  /**
  * short description of attr_five_string
  */
  public static final AttributeKey<Enum> FIFTH_ATTR_FIVE_STRING = enumKey("fifth.attr_five_string");
  public static final class FifthAttrFiveIntValues {
      /** First enum2 value.*/
      public static final long ENUM2_ONE = 1;
      /** Second enum2 value.*/
      public static final long ENUM2_TWO = 2;
  }

  public static final class FifthAttrFiveStringValues {
      /** First enum1 value.*/
      public static final String ENUM1_ONE = "one";
      /** Second enum1 value.*/
      public static final String ENUM1_TWO = "two";
  }

}