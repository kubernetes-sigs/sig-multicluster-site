#!/usr/bin/env python3
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

"""Generate per-version MCS API conformance comparison pages from submitted YAML reports.

Scans the mcs-implementations reports/ subdirectory for reports as YAML files and
generates comparison Markdown pages under its generated/ directory (which is gitignored).

Expected layout:
site-src/
    implementations/
        mcs-implementations/
            reports/
                v0.5.0/submariner/v0.23.0.yaml    (submitted)
                v0.5.0/gke/2026-01-01.yaml        (submitted)
                v0.5.0/gke/2026-07-01.yaml        (submitted)
            generated/                            (generated, gitignored)
                conformance-matrix.md
                v0.5.0/submariner/v0.23.0.md
                v0.5.0/gke/2026-01-01.md
                v0.5.0/gke/2026-07-01.md
"""

import pathlib
from dataclasses import dataclass
from dataclasses import field
from typing import Any

import yaml

import mcs_report

MCS_IMPLEMENTATIONS_DIR = "site-src/implementations/mcs-implementations"


@dataclass
class SubmittedReport:
    """A single submitted conformance report by an implementer"""
    report_yaml: dict[str, Any]
    report_name: str
    generated_report_dir: pathlib.Path

    def row(self, project_dir: pathlib.Path) -> str:
        """Render each table row in the comparisons page"""
        report_link = self.report_path().relative_to(project_dir).as_posix()
        cols: list[str] = []
        cols.append(self.organization())
        cols.append(self.project_col())
        cols.append(self.version())
        cols.append(self.required_tests_col()) # Required Tests
        cols.append(self.total_tests_col()) # Total Tests
        cols.append(f"[{self.report_name}]({report_link})") # Report
        return "| " + " | ".join(cols) + " |"

    def report_path(self) -> pathlib.Path:
        return self.generated_report_dir / f"{self.report_name}.md"

    def generate_report(self, mcs_api_ver: str) -> None:
        """Generates the MCS conformance report for an implementation under generated/"""
        test_sections: list[mcs_report.TestSection] = list(  # Required / Optional section
            map(mcs_report.TestSection.from_yaml_group, self.report_yaml["groups"])
        )

        conformance_report = mcs_report.ConformanceReport( # generates md report
            mcs_api_ver=mcs_api_ver,
            organization=self.organization(),
            project=self.project(),
            project_url=self.url(),
            impl_ver=self.version(),
            sections=test_sections,
        )
        self.generated_report_dir.mkdir(parents=True, exist_ok=True)
        conformance_report.generate(self.report_path())

    def total_tests_col(self) -> str:
        green_tick = " :white_check_mark:" if self.passed() == self.total() else ""
        return f"{self.passed()}/{self.total()}{green_tick}"

    def project_col(self) -> str:
        if self.url():
            return f"[{self.project()}]({self.url()})"
        return self.project()

    def required_tests_col(self) -> str:
        for group in self.report_yaml["groups"]:
            if group["name"] == "Required":
                return mcs_report.TestSection.from_yaml_group(group).passed_summary()
        raise ValueError("Required tests not found")

    def project(self) -> str:
        return self.report_yaml["implementation"].get("project", "")

    def version(self) -> str:
        return self.report_yaml["implementation"].get("version", "")

    def url(self) -> str:
        return self.report_yaml["implementation"].get("url", "")

    def passed(self) -> int:
        return self.report_yaml["passed"]

    def total(self) -> int:
        return self.report_yaml["total"]

    def organization(self) -> str:
        return self.report_yaml["implementation"].get("organization", "")


@dataclass
class ConformanceMatrix:
    """Collects submitted reports by MCS API version and renders the comparison matrix."""
    project_dir: pathlib.Path  # mcs-implementations directory
    reports_by_version: dict[str, list[SubmittedReport]] = field(default_factory=dict)

    @staticmethod
    def header() -> str:
        return (
            "| Organization | Project | Version | Required Tests | Total Tests | Report |\n"
            "|---|---|---|---|---|---|"
        )

    def matrix(self, mcs_api_ver: str, submitted_reports: list[SubmittedReport]) -> str:
        """Render comparisons table for a single MCS version"""
        lines: list[str] = [f"## {mcs_api_ver}"]
        lines.append(self.header())
        for submitted_report in submitted_reports:
            lines.append(submitted_report.row(self.project_dir))
        return "\n".join(lines)

    def add_report(self, mcs_api_ver: str, submitted_report: SubmittedReport) -> None:
        self.reports_by_version.setdefault(mcs_api_ver, []).append(submitted_report)

    def comparison_tables(self) -> str:
        """Render all per-version comparison tables (for /comparisons page) as markdown."""
        self.sort()
        tables: list[str] = []
        # Iterate in descending order of MCS version
        for mcs_api_ver in sorted(self.reports_by_version.keys(), reverse=True):
            tables.append(self.matrix(mcs_api_ver, self.reports_by_version[mcs_api_ver]))
        return "\n\n".join(tables)

    def sort(self) -> None:
        """Sort reports per MCS ver in ascending order of organization name then project name"""
        for submitted_reports in self.reports_by_version.values():
            submitted_reports.sort(key=lambda r: (r.organization().lower(), r.project().lower()))


def main() -> None:
    project_dir = pathlib.Path(MCS_IMPLEMENTATIONS_DIR)
    reports_dir = project_dir / "reports"
    output_dir = project_dir / "generated" # artifacts are generated in this directory
    output_dir.mkdir(parents=True, exist_ok=True) # create generated/ directory

    matrix = ConformanceMatrix(project_dir=project_dir) # generates conformance-matrix.md
    for report_file in sorted(reports_dir.glob("*/*/*.yaml")):
        with open(report_file) as f:
            report_yaml: dict[str, Any] = yaml.safe_load(f)
        mcs_api_ver = report_file.parent.parent.name
        # Mirror per-version reports layout (e.g. v0.5.0/gke/) under the generated directory
        submitted_report = SubmittedReport(
            report_yaml=report_yaml,
            report_name=report_file.stem,
            # e.g. report_file = `<path-prefix>/reports/v0.5.0/gke/2026-07-01.yaml`
            # report_file.parent.relative_to(reports_dir) = `reports/v0.5.0/gke`
            generated_report_dir=output_dir / report_file.parent.relative_to(reports_dir),
        )
        submitted_report.generate_report(mcs_api_ver)
        matrix.add_report(mcs_api_ver, submitted_report)

    output_file = output_dir / "conformance-matrix.md"
    sections = matrix.comparison_tables()
    output_file.write_text(sections)
    print(f"Generated {output_file}")


if __name__ == "__main__":
    main()
