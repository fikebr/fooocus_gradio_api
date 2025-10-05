import logging
from typing import List


logger = logging.getLogger(__name__)


def parse_prompts_file(file_path: str, delimiter: str = "---") -> List[str]:
    """Parse prompts split by delimiter lines.

    Delimiter must be alone on a line; multiline prompts are preserved.
    """
    if not file_path:
        logger.error("parse_prompts_file: missing file_path")
        return []

    try:
        with open(file_path, "r", encoding="utf-8") as handle:
            lines = handle.readlines()
    except Exception as exc:  # noqa: BLE001
        logger.exception("parse_prompts_file: failed to read '%s': %s", file_path, exc)
        return []

    prompts: List[str] = []
    current_lines: List[str] = []
    sep = delimiter.strip()

    def flush_current() -> None:
        if not current_lines:
            return
        text = "".join(current_lines).strip("\n")
        if text.strip():
            prompts.append(text)

    for raw in lines:
        line = raw.rstrip("\n")
        if line.strip() == sep:
            flush_current()
            current_lines = []
            continue
        current_lines.append(raw)

    flush_current()
    logger.debug("parse_prompts_file: parsed %d prompts from '%s'", len(prompts), file_path)
    return prompts
