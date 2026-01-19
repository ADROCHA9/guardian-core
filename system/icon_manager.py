# system/icon_manager.py
import os
import platform
import subprocess
from pathlib import Path


GUARDIAN_SVG = """<svg width="512" height="512" viewBox="0 0 512 512"
xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="ggrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#3fa37a"/>
      <stop offset="100%" stop-color="#1f6b50"/>
    </linearGradient>
  </defs>
  <path
    d="M256 64
       C150 64 64 150 64 256
       C64 362 150 448 256 448
       C330 448 390 406 416 352
       L352 352
       C330 390 296 416 256 416
       C168 416 96 344 96 256
       C96 168 168 96 256 96
       C320 96 372 130 400 176
       L256 176
       L256 288
       L448 288
       C450 278 450 266 450 256
       C450 150 362 64 256 64 Z"
    fill="url(#ggrad)"
  />
</svg>
"""


def ensure_guardian_icon(root_path: str, state_dir: str):
    svg_path = os.path.join(state_dir, "guardian_icon.svg")
    with open(svg_path, "w", encoding="utf-8") as f:
        f.write(GUARDIAN_SVG)

    system = platform.system()

    if system == "Windows":
        _create_windows_shortcut(root_path, svg_path)
    elif system == "Linux":
        _create_linux_desktop(root_path, svg_path)


def _create_windows_shortcut(root_path: str, svg_path: str):
    desktop = Path(os.path.join(os.environ["USERPROFILE"], "Desktop"))
    shortcut = desktop / "GUARDIAN.lnk"

    launcher = os.path.join(root_path, "gui", "app.py")

    ps_script = f'''
$WshShell = New-Object -ComObject WScript.Shell
$Shortcut = $WshShell.CreateShortcut("{shortcut}")
$Shortcut.TargetPath = "python"
$Shortcut.Arguments = "\\"{launcher}\\""
$Shortcut.WorkingDirectory = "{root_path}"
$Shortcut.IconLocation = "{svg_path}"
$Shortcut.Save()
'''

    subprocess.run(
        ["powershell", "-Command", ps_script],
        shell=True
    )


def _create_linux_desktop(root_path: str, svg_path: str):
    desktop_file = os.path.join(
        os.path.expanduser("~"),
        "Desktop",
        "guardian.desktop"
    )

    launcher = os.path.join(root_path, "gui", "app.py")

    content = f"""[Desktop Entry]
Type=Application
Name=GUARDIAN
Exec=python3 "{launcher}"
Icon={svg_path}
Terminal=false
"""

    with open(desktop_file, "w") as f:
        f.write(content)

    os.chmod(desktop_file, 0o755)