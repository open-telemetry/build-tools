from opentelemetry.semconv.model.semantic_attribute import (
    EnumMember,
    RequirementLevel,
    SemanticAttribute,
    StabilityLevel,
)
from opentelemetry.semconv.model.semantic_convention import (
    MetricSemanticConvention,
    SemanticConventionSet,
)

class Error:
    signal: str
    name: str
    message: str

    def __init__(self, signal: str, name: str, message: str):
        self.signal = signal
        self.name = name
        self.message = message

    def __str__(self):
        return f"\t {self.signal} '{self.name}': {self.message}"

class CompatibilityChecker:
    previous_version: str

    def __init__(self, current_semconv: SemanticConventionSet,
        previous_semconv: SemanticConventionSet):
        self.current_semconv = current_semconv
        self.previous_semconv = previous_semconv

    # TODO: attribute templates
    # stability
    # docs
    def check(
        self
    ) -> list[Error]:
        errors = []
        for semconv in self.previous_semconv.models.values():
            for prev_attr in semconv.attributes:
                if prev_attr.is_local and prev_attr.attr_id is not None and prev_attr.ref is None:
                    self._check_attribute(prev_attr, errors)
            if isinstance(semconv, MetricSemanticConvention):
                self._check_metric(semconv, errors)
        return errors


    def _check_attribute(self, prev: SemanticAttribute, errors: list[str]):
        cur = self.current_semconv._lookup_attribute(prev.fqn)
        if (cur is None):
            errors.append(Error("attribute", prev.fqn, "was removed"))
            return

        if prev.stability == StabilityLevel.STABLE:
            if cur.stability != prev.stability:
                errors.append(Error("attribute", prev.fqn, f"stability changed from '{prev.stability}' to '{cur.stability}'"))

            if prev.is_enum:
                if not cur.is_enum:
                    errors.append(Error("attribute", prev.fqn, f"type changed from '{prev.attr_type}' to '{cur.attr_type}'"))
                else:
                    if cur.attr_type.enum_type != prev.attr_type.enum_type:
                        errors.append(Error("attribute", prev.fqn, f"enum type changed from '{prev.attr_type.enum_type}' to '{cur.attr_type.enum_type}'"))
                    for member in prev.attr_type.members:
                        self._check_member(prev.fqn, member, cur.attr_type.members, errors)
            elif cur.attr_type != prev.attr_type:
                errors.append(Error("attribute", prev.fqn, f"type changed from '{prev.attr_type}' to '{cur.attr_type}'"))


    def _check_member(self, fqn: str, prev: EnumMember, members: list[EnumMember], errors: list[str]):
        for member in members:
            if prev.value == member.value:
                return

        errors.append(Error("attribute", fqn, f"enum member with value '{prev.value}' was removed"))


    def _check_metric(self, prev: MetricSemanticConvention, errors: list[str]):
        for cur in self.current_semconv.models.values():
            if isinstance(cur, MetricSemanticConvention) and cur.metric_name == prev.metric_name:
                if prev.stability == StabilityLevel.STABLE:
                    if cur.stability != prev.stability:
                        errors.append(Error("metric", prev.metric_name, f"stability changed from '{prev.stability}' to '{cur.stability}'"))
                    if cur.unit != prev.unit:
                        errors.append(Error("metric", prev.metric_name, f"unit changed from '{prev.unit}' to '{cur.unit}'"))
                    if cur.instrument != prev.instrument:
                        errors.append(Error("metric", prev.metric_name, f"instrument changed from '{prev.instrument}' to '{cur.instrument}'"))
                    self._check_metric_attributes(prev, cur, errors)
                return

        errors.append(Error("metric", prev.metric_name, "was removed"))

    def _check_metric_attributes(self, prev: MetricSemanticConvention, cur: MetricSemanticConvention, errors: list[str]):
        if prev.stability == StabilityLevel.STABLE:
            prev_default_attributes = [attr.fqn for attr in prev.attributes if attr.requirement_level != RequirementLevel.OPT_IN]
            cur_default_attributes = [attr.fqn for attr in cur.attributes if attr.requirement_level != RequirementLevel.OPT_IN]
            if prev_default_attributes != cur_default_attributes:
                errors.append(Error("metric", prev.metric_name, f"attributes changed from '{prev_default_attributes}' to '{cur_default_attributes}'"))
