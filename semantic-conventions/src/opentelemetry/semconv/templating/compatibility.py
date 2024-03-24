from opentelemetry.semconv.model.semantic_attribute import (
    EnumAttributeType,
    EnumMember,
    RequirementLevel,
    SemanticAttribute,
    StabilityLevel,
)
from opentelemetry.semconv.model.semantic_convention import (
    MetricSemanticConvention,
    SemanticConventionSet,
)


class Problem:
    signal: str
    name: str
    message: str
    critical: bool

    def __init__(self, signal: str, name: str, message: str, critical: bool = True):
        self.signal = signal
        self.name = name
        self.message = message
        self.critical = critical

    def __str__(self):
        return f"{self.signal} '{self.name}' {self.message}"

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__

        return False

    def __ne__(self, other):
        return not self.__eq__(other)


class CompatibilityChecker:
    previous_version: str

    def __init__(
        self,
        current_semconv: SemanticConventionSet,
        previous_semconv: SemanticConventionSet,
    ):
        self.current_semconv = current_semconv
        self.previous_semconv = previous_semconv

    def check(self) -> list[Problem]:
        problems = []  # type: list[Problem]
        for semconv in self.previous_semconv.models.values():
            for prev_attr in semconv.attributes_and_templates:
                if (
                    prev_attr.is_local
                    and prev_attr.attr_id is not None
                    and prev_attr.ref is None
                ):
                    self._check_attribute(prev_attr, problems)
            if isinstance(semconv, MetricSemanticConvention):
                self._check_metric(semconv, problems)
        return problems

    def _check_attribute(self, prev: SemanticAttribute, problems: list[Problem]):
        cur = self.current_semconv._lookup_attribute(prev.fqn)
        if cur is None:
            problems.append(Problem("attribute", prev.fqn, "was removed"))
            return

        self._check_stability(
            prev.stability, cur.stability, "attribute", prev.fqn, problems
        )
        if prev.stability == StabilityLevel.STABLE:
            self._check_attribute_type(prev, cur, problems)

        if (
            isinstance(prev.attr_type, EnumAttributeType)
            and
            # this makes mypy happy, we already checked that type is the same for stable attributes
            isinstance(cur.attr_type, EnumAttributeType)
        ):
            for member in prev.attr_type.members:
                self._check_member(prev.fqn, member, cur.attr_type.members, problems)

    def _check_stability(
        self,
        prev: StabilityLevel,
        cur: StabilityLevel,
        signal: str,
        fqn: str,
        problems: list[Problem],
    ):
        if prev == StabilityLevel.STABLE and cur != prev:
            problems.append(
                Problem(signal, fqn, f"stability changed from '{prev}' to '{cur}'")
            )

    def _check_attribute_type(
        self, prev: SemanticAttribute, cur: SemanticAttribute, problems: list[Problem]
    ):
        if isinstance(prev.attr_type, EnumAttributeType):
            if not isinstance(cur.attr_type, EnumAttributeType):
                problems.append(
                    Problem(
                        "attribute",
                        prev.fqn,
                        f"type changed from '{prev.attr_type}' to '{cur.attr_type}'",
                    )
                )
            else:
                # enum type change inevitably causes some values to be removed
                # which will be reported in _check_member method as well.
                # keeping this check to provide more detailed error message
                if cur.attr_type.enum_type != prev.attr_type.enum_type:
                    problems.append(
                        Problem(
                            "attribute",
                            prev.fqn,
                            f"enum type changed from '{prev.attr_type.enum_type}' to '{cur.attr_type.enum_type}'",
                        )
                    )
        elif cur.attr_type != prev.attr_type:
            problems.append(
                Problem(
                    "attribute",
                    prev.fqn,
                    f"type changed from '{prev.attr_type}' to '{cur.attr_type}'",
                )
            )

    def _check_member(
        self,
        fqn: str,
        prev: EnumMember,
        members: list[EnumMember],
        problems: list[Problem],
    ):
        found = False
        for member in members:
            if prev.member_id == member.member_id:
                found = True
                if prev.stability != StabilityLevel.STABLE:
                    # we allow stability and value changes for non-stable members
                    break

                self._check_stability(
                    prev.stability,
                    member.stability,
                    "enum attribute member",
                    f"{fqn}.{prev.member_id}",
                    problems,
                )

                if prev.value != member.value:
                    member_value = (
                        f'"{member.value}"'
                        if isinstance(member.value, str)
                        else member.value
                    )
                    problems.append(
                        Problem(
                            "enum attribute member",
                            f"{fqn}.{prev.member_id}",
                            f"value changed from '{prev.value}' to '{member_value}'",
                        )
                    )
        if not found:
            problems.append(
                Problem(
                    "enum attribute member", f"{fqn}.{prev.member_id}", "was removed"
                )
            )

    def _check_metric(self, prev: MetricSemanticConvention, problems: list[Problem]):
        for cur in self.current_semconv.models.values():
            if (
                isinstance(cur, MetricSemanticConvention)
                and cur.metric_name == prev.metric_name
            ):
                if prev.stability == StabilityLevel.STABLE:
                    self._check_stability(
                        prev.stability,
                        cur.stability,
                        "metric",
                        prev.metric_name,
                        problems,
                    )
                    if cur.unit != prev.unit:
                        problems.append(
                            Problem(
                                "metric",
                                prev.metric_name,
                                f"unit changed from '{prev.unit}' to '{cur.unit}'",
                            )
                        )
                    if cur.instrument != prev.instrument:
                        problems.append(
                            Problem(
                                "metric",
                                prev.metric_name,
                                f"instrument changed from '{prev.instrument}' to '{cur.instrument}'",
                            )
                        )
                    self._check_metric_attributes(prev, cur, problems)
                return

        problems.append(Problem("metric", prev.metric_name, "was removed"))

    def _check_metric_attributes(
        self,
        prev: MetricSemanticConvention,
        cur: MetricSemanticConvention,
        problems: list[Problem],
    ):
        if prev.stability == StabilityLevel.STABLE:
            prev_default_attributes = [
                attr.fqn
                for attr in prev.attributes
                if attr.requirement_level != RequirementLevel.OPT_IN
            ]
            cur_default_attributes = [
                attr.fqn
                for attr in cur.attributes
                if attr.requirement_level != RequirementLevel.OPT_IN
            ]
            if prev_default_attributes != cur_default_attributes:
                # Adding attributes to metrics could be fine if it does not increase number of time series,
                # so we do not consider it as critical problem.
                problems.append(
                    Problem(
                        "metric",
                        prev.metric_name,
                        f"attributes changed from '{prev_default_attributes}' to '{cur_default_attributes}'",
                        False,
                    )
                )
