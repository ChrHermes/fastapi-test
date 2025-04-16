# app/utils/common.py


def format_bytes(size: float, decimals: int = 2) -> str:
    """
    Konvertiert Byte-Größen in ein menschenlesbares Format (z.B. GB, MB).

    Args:
        size: Größe in Bytes
        decimals: Anzahl Nachkommastellen

    Returns:
        Ein string wie "1.5 GB"
    """
    if size == 0:
        return "0 B"

    units = ["B", "KB", "MB", "GB", "TB"]
    index = 0
    while size >= 1024 and index < len(units) - 1:
        size /= 1024
        index += 1

    return f"{size:.{decimals}f} {units[index]}"
