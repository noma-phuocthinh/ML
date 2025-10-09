from pathlib import Path

def getProjectRoot(marker: str = ".git") -> Path:
    """
    Trả về thư mục gốc của dự án (project root).
    - Mặc định sẽ tìm thư mục chứa file `.git` (coi đó là gốc dự án).
    - Nếu không có `.git`, bạn có thể thay marker bằng thư mục đặc trưng khác. Ví dụ: data, ...
    """
    current = Path(__file__).resolve()
    for parent in current.parents:
        if (parent / marker).exists():
            return parent
    return "Ko tìm thấy marker, vui lòng chỉ định marker phù hợp"

