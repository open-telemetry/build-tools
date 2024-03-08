from opentelemetry.semconv.model.utils import ValidatableYamlNode


class UnitMember(ValidatableYamlNode):

    allowed_keys = ("id", "brief", "value")
    mandatory_keys = allowed_keys

    def __init__(self, node, validation_ctx):
        super().__init__(node, validation_ctx)
        self.value = node.get("value")

    @staticmethod
    def parse(members, validation_ctx):
        parsed_members = {}
        for member in members:
            UnitMember.validate_keys(member, validation_ctx)
            unit_member = UnitMember(member, validation_ctx)
            unit_member.validate_values()
            parsed_members[unit_member.id] = unit_member

        return parsed_members
