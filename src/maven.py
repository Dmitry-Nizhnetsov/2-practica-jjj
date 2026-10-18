from __future__ import annotations

import ssl
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET
from dataclasses import dataclass


class MavenError(Exception):
    """Ошибка при работе с Maven-репозиторием."""


@dataclass(frozen=True)
class Dependency:


    group_id: str
    artifact_id: str
    version: str

    def full_name(self) -> str:
        return f"{self.group_id}:{self.artifact_id}:{self.version}"


def parse_package_name(package_name: str) -> tuple[str, str, str]:

    parts = package_name.split(":")
    if len(parts) != 3:
        raise MavenError(
            f"Неверный формат пакета '{package_name}'. "
            f"Ожидается 'group:artifact:version'"
        )
    return parts[0].strip(), parts[1].strip(), parts[2].strip()


def build_pom_url(repo_url: str, group_id: str, artifact_id: str, version: str) -> str:

    group_path = group_id.replace(".", "/")
    base = repo_url.rstrip("/")
    return f"{base}/{group_path}/{artifact_id}/{version}/{artifact_id}-{version}.pom"


def fetch_pom(url: str) -> str:

    context = ssl._create_unverified_context()
    try:
        with urllib.request.urlopen(url, timeout=10, context=context) as response:
            raw = response.read()
    except urllib.error.HTTPError as exc:
        raise MavenError(f"HTTP {exc.code} при загрузке {url}") from exc
    except urllib.error.URLError as exc:
        raise MavenError(f"Ошибка сети: {exc.reason}") from exc
    return raw.decode("utf-8")


def parse_pom(xml_text: str) -> list[Dependency]:

    try:
        root = ET.fromstring(xml_text)
    except ET.ParseError as exc:
        raise MavenError(f"Неверный XML в POM: {exc}") from exc

    ns = "http://maven.apache.org/POM/4.0.0"

    dependencies: list[Dependency] = []

    deps_section = root.find(f"{{{ns}}}dependencies")
    if deps_section is None:
        deps_section = root.find("dependencies")
    if deps_section is None:
        return dependencies

    for dep_elem in deps_section:
        group = _find_text(dep_elem, "groupId", ns)
        artifact = _find_text(dep_elem, "artifactId", ns)
        version = _find_text(dep_elem, "version", ns) or "unknown"

        if group and artifact:
            dependencies.append(Dependency(group, artifact, version))

    return dependencies


def _find_text(elem: ET.Element, tag: str, namespace: str) -> str | None:

    child = elem.find(f"{{{namespace}}}{tag}")
    if child is None:
        child = elem.find(tag)
    if child is None or child.text is None:
        return None
    return child.text.strip()


def get_direct_dependencies(repo_url: str, package_name: str) -> list[Dependency]:

    group_id, artifact_id, version = parse_package_name(package_name)
    url = build_pom_url(repo_url, group_id, artifact_id, version)
    xml_text = fetch_pom(url)
    return parse_pom(xml_text)