import io
import zipfile
import re
import os

IGNORED_DIRS = {
    ".git",
    "node_modules",
    "dist",
    "build",
    "__pycache__",
    ".venv",
}

ALLOWED_EXTENSIONS = {
    ".py",
    ".js",
    ".vue",
    ".jsx",
    ".ts",
    ".tsx",
    ".html",
    ".css",
    ".json",
    ".md",
}

# Helpers
def resolve_js_import(source, imported, paths):
    if not imported.startswith("."):
        return None

    base = os.path.normpath(
        os.path.join(
            os.path.dirname(source),
            imported
        )
    )

    candidates = [
        base,
        base + ".js",
        base + ".vue",
        base + ".ts",
        os.path.join(base, "index.js"),
    ]

    for candidate in candidates:
        candidate = candidate.replace("\\", "/")

        if candidate in paths:
            return candidate

    return None

# 2nd helper
def resolve_python_import(imported, paths):
    module_path = imported.replace(".", "/")

    candidates = [
        module_path + ".py",
        module_path + "/__init__.py",
    ]

    for candidate in candidates:
        if candidate in paths:
            return candidate

    return None

def extract_imports(files):
    paths = {
        file["path"]
        for file in files
    }

    relationships = []

    for file in files:
        source = file["path"]
        content = file["content"]

        # JavaScript / Vue imports
        js_imports = re.findall(
            r'import\s+.*?\s+from\s+[\'"](.+?)[\'"]',
            content
        )

        for imported in js_imports:
            target = resolve_js_import(source, imported, paths)

            if target:
                relationships.append({
                    "source": source,
                    "target": target
                })

        # Python imports
        py_imports = re.findall(
            r'(?:from|import)\s+([a-zA-Z0-9_./]+)',
            content
        )

        for imported in py_imports:
            target = resolve_python_import(imported, paths)

            if target:
                relationships.append({
                    "source": source,
                    "target": target
                })

    return relationships

def scan_project(zip_bytes):
    files = []

    with zipfile.ZipFile(io.BytesIO(zip_bytes)) as archive:
        for info in archive.infolist():
            if info.is_dir():
                continue

            parts = info.filename.split("/")

            if any(part in IGNORED_DIRS for part in parts):
                continue

            filename = parts[-1]

            if not any(
                filename.endswith(extension)
                for extension in ALLOWED_EXTENSIONS
            ):
                continue

            # Read file content too
            content = archive.read(info).decode(
                "utf-8",
                errors="ignore"
            )

            files.append({
                "path": info.filename,
                "size": info.file_size,
                "content": content[:15000],
            })

    return files