#!/usr/bin/env python3
"""Generate the animated featured-project cards used by the profile README."""

from html import escape
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "projects"
FONT = "Segoe UI, Ubuntu, Helvetica, Arial, sans-serif"

PROJECTS = [
    {
        "file": "campus-pilot.svg",
        "title": "CampusPilot AI",
        "eyebrow": "JAVA AI AGENT · FEATURED",
        "description": (
            "A WeChat-native campus planning agent with multi-turn memory, "
            "RAG, multimodal interaction, a 12-task DAG and evaluator-driven output."
        ),
        "tags": ["Java 21", "Spring Boot", "Qwen", "RAG", "Task DAG"],
        "accent": "#F4795B",
        "petal": "#FFB49D",
    },
    {
        "file": "wechat-bot.svg",
        "title": "WeChat iLink Multimodal Bot",
        "eyebrow": "MULTIMODAL · TOOL USE",
        "description": (
            "A Spring Boot bot for text, images and voice, combining Function "
            "Calling, Skills, local RAG, live data and parallel tool execution."
        ),
        "tags": ["WeChat", "DashScope", "Function Calling", "ASR / TTS"],
        "accent": "#7FA36B",
        "petal": "#BBD6AD",
    },
    {
        "file": "worldmuse.svg",
        "title": "WorldMuse · 云览天下",
        "eyebrow": "HARMONYOS · AWARD WINNER",
        "description": (
            "A native HarmonyOS 6 cloud-museum experience for collections, "
            "history quizzes and timelines — awarded by the 2025 developer program."
        ),
        "tags": ["HarmonyOS 6", "ArkTS", "ArkUI", "Cultural Heritage"],
        "accent": "#9986D4",
        "petal": "#C9BDF0",
    },
]


def chip(x: int, y: int, label: str, accent: str) -> tuple[str, int]:
    width = 20 + max(44, round(len(label) * 7.2))
    svg = (
        f'<g transform="translate({x},{y})">'
        f'<rect width="{width}" height="24" rx="12" fill="{accent}" fill-opacity="0.09" '
        f'stroke="{accent}" stroke-opacity="0.48"/>'
        f'<text x="{width / 2:g}" y="16" text-anchor="middle" font-size="11" '
        f'font-weight="600" fill="{accent}">{escape(label)}</text></g>'
    )
    return svg, width


def wrap_words(text: str, limit: int = 96) -> list[str]:
    lines: list[str] = []
    current = ""
    for word in text.split():
        candidate = f"{current} {word}".strip()
        if current and len(candidate) > limit:
            lines.append(current)
            current = word
        else:
            current = candidate
    if current:
        lines.append(current)
    return lines[:2]


def card(project: dict) -> str:
    accent = project["accent"]
    tags = []
    x = 76
    for label in project["tags"]:
        item, width = chip(x, 132, label, accent)
        tags.append(item)
        x += width + 9

    description = wrap_words(project["description"])
    description_svg = "".join(
        f'<text x="76" y="{83 + index * 19}" font-size="13" fill="#8b949e">{escape(line)}</text>'
        for index, line in enumerate(description)
    )

    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 860 170" width="860" height="170" font-family="{FONT}">
  <title>{escape(project["title"])} — featured project</title>
  <defs>
    <linearGradient id="wash" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="{accent}" stop-opacity="0.11"/>
      <stop offset="1" stop-color="{accent}" stop-opacity="0.025"/>
    </linearGradient>
  </defs>
  <rect x="1" y="1" width="858" height="168" rx="18" fill="url(#wash)" stroke="{accent}" stroke-opacity="0.38" stroke-width="1.2"/>
  <g transform="translate(38,85)">
    <g>
      <animateTransform attributeName="transform" type="rotate" from="0" to="360" dur="18s" repeatCount="indefinite"/>
      <ellipse rx="8" ry="23" fill="{project["petal"]}" transform="rotate(0) translate(0,-17)"/>
      <ellipse rx="8" ry="23" fill="{project["petal"]}" transform="rotate(72) translate(0,-17)"/>
      <ellipse rx="8" ry="23" fill="{project["petal"]}" transform="rotate(144) translate(0,-17)"/>
      <ellipse rx="8" ry="23" fill="{project["petal"]}" transform="rotate(216) translate(0,-17)"/>
      <ellipse rx="8" ry="23" fill="{project["petal"]}" transform="rotate(288) translate(0,-17)"/>
    </g>
    <circle r="10" fill="{accent}"/>
    <circle r="4" fill="#FFF2D8"/>
  </g>
  <g opacity="0">
    <animate attributeName="opacity" from="0" to="1" dur="0.7s" fill="freeze"/>
    <text x="76" y="27" font-size="10" letter-spacing="1.7" fill="{accent}">{escape(project["eyebrow"])}</text>
    <text x="76" y="55" font-size="23" font-weight="700" fill="{accent}">{escape(project["title"])}</text>
    {description_svg}
    {''.join(tags)}
  </g>
  <g transform="translate(821,85)" fill="none" stroke="{accent}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" opacity="0.72">
    <path d="M-9 -9 L0 0 L-9 9"/>
    <path d="M-20 0 H0"/>
    <animateTransform attributeName="transform" type="translate" values="821 85;826 85;821 85" dur="2.2s" repeatCount="indefinite"/>
  </g>
</svg>
'''


def main() -> None:
    OUT.mkdir(exist_ok=True)
    expected = set()
    for project in PROJECTS:
        path = OUT / project["file"]
        path.write_text(card(project), encoding="utf-8")
        expected.add(path.name)
    for path in OUT.glob("*.svg"):
        if path.name not in expected:
            path.unlink()
    print(f"{len(expected)} project cards written")


if __name__ == "__main__":
    main()
