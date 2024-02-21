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

        if prev.stability == StabilityLevel.STABLE:
            if cur.stability != prev.stability:
                problems.append(
                    Problem(
                        "attribute",
                        prev.fqn,
                        f"stability changed from '{prev.stability}' to '{cur.stability}'",
                    )
                )

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
                    if cur.attr_type.enum_type != prev.attr_type.enum_type:
                        problems.append(
                            Problem(
                                "attribute",
                                prev.fqn,
                                f"enum type changed from '{prev.attr_type.enum_type}' to '{cur.attr_type.enum_type}'",
                            )
                        )
                    for member in prev.attr_type.members:
                        self._check_member(
                            prev.fqn, member, cur.attr_type.members, problems
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
        for member in members:
            if prev.value == member.value:
                return

        problems.append(
            Problem(
                "attribute", fqn, f"enum member with value '{prev.value}' was removed"
            )
        )

    def _check_metric(self, prev: MetricSemanticConvention, problems: list[Problem]):
        for cur in self.current_semconv.models.values():
            if (
                isinstance(cur, MetricSemanticConvention)
                and cur.metric_name == prev.metric_name
            ):
                if prev.stability == StabilityLevel.STABLE:
                    if cur.stability != prev.stability:
                        problems.append(
                            Problem(
                                "metric",
                                prev.metric_name,
                                f"stability changed from '{prev.stability}' to '{cur.stability}'",
                            )
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
