# Copyright The Kubernetes Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Render a single MCS API conformance report as a Markdown page.

Provides the data structures that turn one submitted conformance YAML report
into a detailed Markdown page (similar to the suite's report.html). Used by
generate-conformance-matrix.py, which links to each generated page from the
comparison matrix.
"""

from dataclasses import dataclass
from dataclasses import field
import html
import pathlib
from typing import Any

@dataclass
class TestRow:
    """A single test row in the HTML conformance report."""
    result: dict[str, Any] # Each test result `groups[*].tests[i]`

    def row(self) -> str:
        cols: list[str] = []
        cols.append(self.conformant_col())
        cols.append(self.labels_col())
        cols.append(self.description_col())
        return "| " + " | ".join(cols) + " |"

    def conformant_col(self) -> str:
        if self.skipped():
            return ':octicons-skip-16: Skipped'
        if self.failed():
            return ":warning: Unknown"
        if self.conformant():
            return ":white_check_mark: Yes"
        return ":x: No"

    def labels_col(self) -> str:
        return " ".join(f"`{label}`" for label in self.labels())

    def description_col(self) -> str:
        if not self.description_url():
            return self.description()
        return f"[{self.description()}]({self.description_url()})"

    def failed(self) -> bool:
        return self.result["failed"]

    def skipped(self) -> bool:
        return self.result["skipped"]

    def conformant(self) -> bool:
        return self.result["conformant"]

    def passed(self) -> bool:
        return self.result["passed"]

    def description(self) -> str:
        return html.escape(self.result["desc"])

    def description_url(self) -> str | None:
        return self.result.get("ref")

    def labels(self) -> list[str]:
        return self.result.get("labels", [])


@dataclass
class TestSection:
    """A named section (Required / Optional) of the HTML report."""
    name: str
    tests: list[TestRow] = field(default_factory=list)

    @staticmethod
    def from_yaml_group(group_yaml: dict) -> "TestSection": # groups[i] of yaml report
        tests = [TestRow(testrow) for testrow in group_yaml["tests"]]
        return TestSection(group_yaml["name"], tests)
    
    @staticmethod
    def header() -> str:
        return (
            "| Conformant | Labels | Description |\n"
            "|---|---|---|"
        )
    
    def section(self) -> str:
        lines: list[str] = []
        lines.append(f"## {self.name} Tests")
        lines.append(f"Passed: {self.passed_summary()}\n")
        lines.append(self.header())
        for test in self.tests:
            lines.append(test.row())
        return "\n".join(lines)

    def passed_counts(self) -> tuple[int, int]:
        passed = sum(1 for test in self.tests if test.passed())
        total = len(self.tests)
        return passed, total

    def passed_summary(self) -> str:
        passed, total = self.passed_counts()
        icon = ""
        if passed == total:
            icon = " :white_check_mark:"
        elif self.name == "Required":
            assert passed > 0, "Required tests should have at least one passed test"
            icon = " :warning:"
        return f"{passed}/{total}{icon}"


@dataclass
class ConformanceReport:
    """Generates detailed conformance report similar to report.html"""
    mcs_api_ver: str
    organization: str
    project: str
    project_url: str
    impl_ver: str
    sections: list[TestSection] = field(default_factory=list)

    def report(self) -> str:
        lines: list[str] = []
        lines.append(f"# {self.project} MCS API Conformance Report")
        lines.append(f"* MCS API Version: {self.mcs_api_ver}")
        lines.append(f"* Organization: {self.organization}")
        lines.append(f"* Project: [{self.project}]({self.project_url})")
        lines.append(f"* Implementation Version: {self.impl_ver}")
        for section in self.sections:
            lines.append(section.section())
        return "\n\n".join(lines)

    def generate(self, path: pathlib.Path) -> None:
        with open(path, "w") as f:
            f.write(self.report())
