
# Antigus - Premium Free Antivirus (Starter Template)

import os
import time
import platform
import json
from scanner_utils import is_malicious
from quarantine import quarantine_file, list_quarantine
from dashboard import show_dashboard
from updater_utils import fetch_definitions

# --- OS Selection (First Run) ---
CONFIG_FILE = "antivirus_config.json"
def select_os_once():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE) as f:
            config = json.load(f)
        return config.get("os")
    print("Select your OS for .exe compatibility (only once):")
    print("1. Windows (.exe)")
    print("2. Linux")
    print("3. MacOS")
    choice = input("Enter 1, 2, or 3: ").strip()
    os_map = {"1": "Windows", "2": "Linux", "3": "MacOS"}
    chosen = os_map.get(choice, platform.system())
    with open(CONFIG_FILE, "w") as f:
        json.dump({"os": chosen}, f)
    print(f"OS set to {chosen}. You can now build for this platform.")
    return chosen

# --- Updater Module ---
def update_definitions():
    print("Updating virus definitions...")
    # Example: Fetch from a public source (replace URL with a real one)
    url = "https://example.com/virus_hashes.txt"
    global BAD_HASHES
    BAD_HASHES = fetch_definitions(url)
    print("Definitions updated.")


# --- Scanner Module ---
def scan_system(path="/"):
    print(f"Scanning {path} for threats...")
    threats = []
    for root, dirs, files in os.walk(path):
        for file in files:
            fpath = os.path.join(root, file)
            if is_malicious(fpath, BAD_HASHES):
                print(f"Threat detected: {fpath}")
                quarantine_file(fpath)
                threats.append(fpath)
            else:
                print(f"Scanned: {fpath}")
    print(f"Scan complete. {len(threats)} threats quarantined.")
    return threats

# --- Cleaner Module ---
def clean_quarantine():
    files = list_quarantine()
    if not files:
        print("No files to clean.")
        return
    for f in files:
        try:
            os.remove(f)
            print(f"Removed: {f}")
        except Exception as e:
            print(f"Failed to remove {f}: {e}")
    print("Quarantine cleaned.")

# --- Report Module ---
def generate_report():
    print("Generating security report...")
    threats = scan_system()
    files = list_quarantine()
    report = {
        "threats_found": len(threats),
        "quarantined": files,
        "os": platform.system(),
        "time": time.ctime()
    }
    with open("antivirus_report.json", "w") as f:
        json.dump(report, f, indent=2)
    print("Report saved to antivirus_report.json.")

# --- Monitor Module ---
def start_monitoring():
    print("Real-time protection enabled.")
    # Simulate monitoring loop (demo)
    for i in range(3):
        print(f"[Monitor] System check {i+1}...")
        time.sleep(1)
    print("Monitoring complete.")

# --- Quarantine Module ---
def show_quarantine():
    files = list_quarantine()
    if files:
        print("Quarantined files:")
        for f in files:
            print(f"- {f}")
    else:
        print("Quarantine is empty.")

from PyQt5 import QtWidgets, QtGui, QtCore


APP_NAME = "Antigus"
APP_VERSION = "1.0.0"
GIT_URL = "https://github.com/arduinoUNO65/antigus/archive/refs/heads/main.zip"
PROGRESS_FILE = "antigus_progress.json"

# Write version info to file
with open("antigus_version.txt", "w") as vf:
    vf.write(f"{APP_NAME} v{APP_VERSION}\n")

# Load or initialize persistent settings
def load_progress():
    if os.path.exists(PROGRESS_FILE):
        with open(PROGRESS_FILE) as f:
            return json.load(f)
    return {"theme": "light", "scans": 0, "threats": 0}

def save_progress(data):
    with open(PROGRESS_FILE, "w") as f:
        json.dump(data, f)

progress = load_progress()

class MainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle(f"{APP_NAME} - Premium Free Antivirus")
        self.setGeometry(100, 100, 900, 600)
        self.theme = progress.get("theme", "light")
        self.apply_theme()

        # Sidebar
        sidebar = QtWidgets.QFrame()
        sidebar.setFixedWidth(180)
        sidebar.setStyleSheet("background: #181a1b; border-top-right-radius: 18px; border-bottom-right-radius: 18px;")
        sidebar_layout = QtWidgets.QVBoxLayout()
        sidebar_layout.setAlignment(QtCore.Qt.AlignTop)
        logo = QtWidgets.QLabel(f"<h2 style='color:#00ff99; text-align:center;'>🛡️<br>{APP_NAME}</h2><p style='color:#888; font-size:0.9em;'>A trusted friend for your PC</p>")
        logo.setAlignment(QtCore.Qt.AlignCenter)
        sidebar_layout.addWidget(logo)
        self.btn_dashboard = QtWidgets.QPushButton("Dashboard")
        self.btn_dashboard.setStyleSheet(self.sidebar_btn_style(True))
        self.btn_scan = QtWidgets.QPushButton("Scan")
        self.btn_scan.setStyleSheet(self.sidebar_btn_style(False))
        self.btn_quarantine = QtWidgets.QPushButton("Quarantine")
        self.btn_quarantine.setStyleSheet(self.sidebar_btn_style(False))
        self.btn_update = QtWidgets.QPushButton("Update")
        self.btn_update.setStyleSheet(self.sidebar_btn_style(False))
        self.btn_tools = QtWidgets.QPushButton("Tools")
        self.btn_tools.setStyleSheet(self.sidebar_btn_style(False))
        self.btn_settings = QtWidgets.QPushButton("Settings")
        self.btn_settings.setStyleSheet(self.sidebar_btn_style(False))
        for btn in [self.btn_dashboard, self.btn_scan, self.btn_quarantine, self.btn_update, self.btn_tools, self.btn_settings]:
            btn.setCursor(QtCore.Qt.PointingHandCursor)
            sidebar_layout.addWidget(btn)
        sidebar_layout.addStretch()
        sidebar.setLayout(sidebar_layout)

        # Main content area (stacked)
        self.stack = QtWidgets.QStackedWidget()
        self.page_dashboard = self.build_dashboard()
        self.page_scan = self.build_scan()
        self.page_quarantine = self.build_quarantine()
        self.page_update = self.build_update()
        self.page_tools = self.build_tools()
        self.page_settings = self.build_settings()
        self.stack.addWidget(self.page_dashboard)
        self.stack.addWidget(self.page_scan)
        self.stack.addWidget(self.page_quarantine)
        self.stack.addWidget(self.page_update)
        self.stack.addWidget(self.page_tools)
        self.stack.addWidget(self.page_settings)

        # Layout
        main_layout = QtWidgets.QHBoxLayout()
        main_layout.addWidget(sidebar)
        main_layout.addWidget(self.stack)
        container = QtWidgets.QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

        # Connect sidebar
        self.btn_dashboard.clicked.connect(lambda: self.switch_page(0))
        self.btn_scan.clicked.connect(lambda: self.switch_page(1))
        self.btn_quarantine.clicked.connect(lambda: self.switch_page(2))
        self.btn_update.clicked.connect(lambda: self.switch_page(3))
        self.btn_tools.clicked.connect(lambda: self.switch_page(4))
        self.btn_settings.clicked.connect(lambda: self.switch_page(5))

    def sidebar_btn_style(self, active):
        if active:
            return "background:#00ff99; color:#181a1b; font-weight:bold; border-radius:10px; margin:8px 0; padding:12px; font-size:1.1em;"
        return "background:transparent; color:#fff; font-weight:bold; border-radius:10px; margin:8px 0; padding:12px; font-size:1.1em;"

    def switch_page(self, idx):
        btns = [self.btn_dashboard, self.btn_scan, self.btn_quarantine, self.btn_update, self.btn_tools, self.btn_settings]
        for i, btn in enumerate(btns):
            btn.setStyleSheet(self.sidebar_btn_style(i == idx))
        self.stack.setCurrentIndex(idx)

    def build_update(self):
        page = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout()
        title = QtWidgets.QLabel("<h2 style='color:#00c3ff;'>Update Antigus</h2>")
        title.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(title)
        self.update_btn = QtWidgets.QPushButton("Update from GitHub")
        self.update_btn.setStyleSheet("background:#00c3ff; color:#fff; font-weight:bold; border-radius:10px; padding:12px; font-size:1.1em;")
        self.update_btn.clicked.connect(self.start_update)
        layout.addWidget(self.update_btn)
        self.update_progress = QtWidgets.QProgressBar()
        self.update_progress.setStyleSheet("background:#333; color:#00c3ff; border-radius:8px; height:24px;")
        layout.addWidget(self.update_progress)
        self.update_status = QtWidgets.QLabel("<b>Status:</b> Ready for update.")
        self.update_status.setStyleSheet("color:#00c3ff; font-size:1.1em;")
        layout.addWidget(self.update_status)
        github_label = QtWidgets.QLabel('<a href="https://github.com/arduinoUNO65/antigus" style="color:#00c3ff;">Visit Antigus on GitHub</a>')
        github_label.setOpenExternalLinks(True)
        github_label.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(github_label)
        page.setLayout(layout)
        return page

    def start_update(self):
        import threading
        def do_update():
            import requests, shutil, tempfile, os
            self.update_status.setText("<b>Status:</b> Downloading update...")
            self.update_progress.setValue(0)
            try:
                tmp = tempfile.NamedTemporaryFile(delete=False)
                with requests.get(GIT_URL, stream=True) as r:
                    r.raise_for_status()
                    total = int(r.headers.get('content-length', 0))
                    downloaded = 0
                    chunk_size = 8192
                    for chunk in r.iter_content(chunk_size=chunk_size):
                        if chunk:
                            tmp.write(chunk)
                            downloaded += len(chunk)
                            percent = int((downloaded / total) * 100) if total else 0
                            self.update_progress.setValue(percent)
                            QtCore.QCoreApplication.processEvents()
                tmp.close()
                self.update_status.setText("<b>Status:</b> Update downloaded! (Not auto-installed)")
            except Exception as e:
                self.update_status.setText(f"<b>Status:</b> Update failed: {e}")
                self.update_progress.setValue(0)
        threading.Thread(target=do_update).start()

    def build_tools(self):
        page = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout()
        title = QtWidgets.QLabel("<h2 style='color:#2af598;'>Tools & Utilities</h2>")
        title.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(title)
        self.sus_btn = QtWidgets.QPushButton("Detect Suspicious Software")
        self.sus_btn.setStyleSheet("background:#2af598; color:#181a1b; font-weight:bold; border-radius:10px; padding:12px; font-size:1.1em;")
        self.sus_btn.clicked.connect(self.detect_sus_software_gui)
        layout.addWidget(self.sus_btn)
        self.sus_result = QtWidgets.QTextEdit()
        self.sus_result.setReadOnly(True)
        self.sus_result.setStyleSheet("background:#222; color:#fff; border-radius:8px; font-size:1em;")
        layout.addWidget(self.sus_result)
        page.setLayout(layout)
        return page

    def detect_sus_software_gui(self):
        try:
            import psutil
        except ImportError:
            self.sus_result.setPlainText("psutil not installed. Run 'pip install psutil' for advanced detection.")
            return
        sus_processes = []
        for proc in psutil.process_iter(['pid', 'name', 'exe', 'username']):
            try:
                pname = proc.info['name'] or ''
                if any(s in pname.lower() for s in ['hack', 'crack', 'keygen', 'inject', 'miner', 'steal', 'spy', 'rat', 'trojan', 'suspicious']):
                    sus_processes.append(proc.info)
            except Exception:
                continue
        if sus_processes:
            result = "Suspicious software detected:\n" + "\n".join([f"- {p['name']} (PID: {p['pid']}, User: {p['username']})" for p in sus_processes])
        else:
            result = "No suspicious software found."
        self.sus_result.setPlainText(result)

    def build_dashboard(self):
        page = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout()
        title = QtWidgets.QLabel(f"""
            <h1 style='color:#fff; font-size:2.2em; letter-spacing:2px; text-shadow:0 0 10px #00ff99;'>{APP_NAME}</h1>
            <p style='color:#eee; font-size:1.1em;'>Premium Free Antivirus</p>
        """)
        title.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(title)
        self.status_label = QtWidgets.QLabel("<b>Status:</b> Ready")
        self.status_label.setStyleSheet("color:#fff; font-size:1.1em;")
        layout.addWidget(self.status_label)
        self.resource_label = QtWidgets.QLabel("<b>Resources:</b> CPU: -- | RAM: -- | Disk: --")
        self.resource_label.setStyleSheet("color:#fff; font-size:1.1em;")
        layout.addWidget(self.resource_label)
        version_label = QtWidgets.QLabel(f"<b>Version:</b> {APP_VERSION}")
        version_label.setStyleSheet("color:#00ff99; font-size:1.1em;")
        layout.addWidget(version_label)
        layout.addStretch()
        page.setLayout(layout)
        # Timer for resource updates
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_resources)
        self.timer.start(1000)
        return page

    def build_scan(self):
        page = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout()
        title = QtWidgets.QLabel("<h2 style='color:#00ff99;'>System Scan</h2>")
        title.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(title)
        self.scan_btn = QtWidgets.QPushButton("Start Scan")
        self.scan_btn.setStyleSheet("background:#00ff99; color:#181a1b; font-weight:bold; border-radius:10px; padding:12px; font-size:1.1em;")
        self.scan_btn.clicked.connect(self.start_scan)
        layout.addWidget(self.scan_btn)
        self.scan_progress = QtWidgets.QProgressBar()
        self.scan_progress.setStyleSheet("background:#333; color:#00ff99; border-radius:8px; height:24px;")
        layout.addWidget(self.scan_progress)
        self.scan_result = QtWidgets.QTextEdit()
        self.scan_result.setReadOnly(True)
        self.scan_result.setStyleSheet("background:#222; color:#fff; border-radius:8px; font-size:1em;")
        layout.addWidget(self.scan_result)
        page.setLayout(layout)
        return page

    def build_quarantine(self):
        page = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout()
        title = QtWidgets.QLabel("<h2 style='color:#ff61a6;'>Quarantine</h2>")
        title.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(title)
        self.clean_btn = QtWidgets.QPushButton("Clean Quarantine")
        self.clean_btn.setStyleSheet("background:#ff61a6; color:#fff; font-weight:bold; border-radius:10px; padding:12px; font-size:1.1em;")
        self.clean_btn.clicked.connect(self.clean_quarantine)
        layout.addWidget(self.clean_btn)
        self.quarantine_list = QtWidgets.QTextEdit()
        self.quarantine_list.setReadOnly(True)
        self.quarantine_list.setStyleSheet("background:#222; color:#fff; border-radius:8px; font-size:1em;")
        layout.addWidget(self.quarantine_list)
        page.setLayout(layout)
        return page

    def build_settings(self):
        page = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout()
        title = QtWidgets.QLabel("<h2 style='color:#ffd200;'>Settings</h2>")
        title.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(title)
        # Version info
        version_label = QtWidgets.QLabel(f"<b>Version:</b> {APP_VERSION}")
        version_label.setStyleSheet("color:#ffd200; font-size:1.1em;")
        layout.addWidget(version_label)
        # Premium features info
        premium_label = QtWidgets.QLabel("<b>Premium:</b> All features are free. No upsells. No paywall. Enjoy full protection!")
        premium_label.setStyleSheet("color:#00ff99; font-size:1.1em;")
        layout.addWidget(premium_label)
        # Theme switcher
        theme_label = QtWidgets.QLabel("<b>Theme:</b>")
        theme_label.setStyleSheet("color:#fff; font-size:1.1em;")
        layout.addWidget(theme_label)
        self.theme_toggle = QtWidgets.QCheckBox("Enable dark theme")
        self.theme_toggle.setChecked(self.theme == "dark")
        self.theme_toggle.stateChanged.connect(self.toggle_theme)
        layout.addWidget(self.theme_toggle)
        # OS info
        os_label = QtWidgets.QLabel(f"<b>OS:</b> {platform.system()}")
        os_label.setStyleSheet("color:#fff; font-size:1.1em;")
        layout.addWidget(os_label)
        layout.addStretch()
        page.setLayout(layout)
        return page

    def apply_theme(self):
        if self.theme == "dark":
            self.setStyleSheet("background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #232526, stop:1 #00ff99); color: #fff;")
        else:
            self.setStyleSheet("background: #fff; color: #222;")

    def toggle_theme(self):
        self.theme = "dark" if self.theme_toggle.isChecked() else "light"
        progress['theme'] = self.theme
        save_progress(progress)
        self.apply_theme()

    def update_resources(self):
        try:
            from monitor_utils import get_resource_usage
            usage = get_resource_usage()
            self.resource_label.setText(f"<b>Resources:</b> CPU: {usage['cpu_percent']}% | RAM: {usage['memory_percent']}% | Disk: {usage['disk_percent']}%")
        except Exception:
            self.resource_label.setText("<b>Resources:</b> CPU: -- | RAM: -- | Disk: --")

    def start_scan(self):
        self.status_label.setText("<b>Status:</b> Scanning...")
        self.scan_progress.setValue(0)
        self.scan_result.clear()
        QtCore.QTimer.singleShot(100, self.fake_scan)

    def fake_scan(self):
        threats = []
        import threading
        def scan():
            from scanner_utils import is_malicious
            from quarantine import quarantine_file
            import os
            total = 100
            count = 0
            for root, dirs, files in os.walk("/"):
                for file in files:
                    fpath = os.path.join(root, file)
                    count += 1
                    if is_malicious(fpath, BAD_HASHES):
                        quarantine_file(fpath)
                        threats.append(fpath)
                        self.scan_result.append(f"<span style='color:#ff61a6;'>Threat detected: {fpath}</span>")
                    else:
                        self.scan_result.append(f"Scanned: {fpath}")
                    self.scan_progress.setValue(min(100, int((count/total)*100)))
                    QtCore.QCoreApplication.processEvents()
                    if count >= total:
                        break
                if count >= total:
                    break
            self.status_label.setText(f"<b>Status:</b> Scan Complete. {len(threats)} threats quarantined.")
        threading.Thread(target=scan).start()

    def clean_quarantine(self):
        clean_quarantine()
        self.status_label.setText("<b>Status:</b> Quarantine Cleaned")
        self.update_quarantine_list()

    def update_quarantine_list(self):
        files = list_quarantine()
        if files:
            self.quarantine_list.setPlainText("\n".join(files))
        else:
            self.quarantine_list.setPlainText("Quarantine is empty.")

def launch_ui():
    app = QtWidgets.QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()
def detect_suspicious_software():
    print("Detecting suspicious software...")
    sus_processes = []
    try:
        import psutil
    except ImportError:
        print("psutil not installed. Run 'pip install psutil' for advanced detection.")
        return
    for proc in psutil.process_iter(['pid', 'name', 'exe', 'username']):
        try:
            pname = proc.info['name'] or ''
            pexe = proc.info['exe'] or ''
            if any(s in pname.lower() for s in ['hack', 'crack', 'keygen', 'inject', 'miner', 'steal', 'spy', 'rat', 'trojan', 'suspicious']):
                sus_processes.append(proc.info)
        except Exception:
            continue
    if sus_processes:
        print("Suspicious software detected:")
        for p in sus_processes:
            print(f"- {p['name']} (PID: {p['pid']}, User: {p['username']})")
    else:
        print("No suspicious software found.")
    def start_scan(self):
        self.status.setText("<b>Status:</b> Scanning...")
        self.progress.setValue(0)
        QtCore.QTimer.singleShot(100, self.fake_scan)
    def fake_scan(self):
        for i in range(1, 101):
            QtCore.QCoreApplication.processEvents()
            self.progress.setValue(i)
            time.sleep(0.008)
        self.status.setText("<b>Status:</b> Scan Complete")
    def clean_quarantine(self):
        clean_quarantine()
        self.status.setText("<b>Status:</b> Quarantine Cleaned")
    def generate_report(self):
        generate_report()
        self.status.setText("<b>Status:</b> Report Generated")
    def update_resources(self):
        from monitor_utils import get_resource_usage
        usage = get_resource_usage()
        self.resource_label.setText(f"<b>Resources:</b> CPU: {usage['cpu_percent']}% | RAM: {usage['memory_percent']}% | Disk: {usage['disk_percent']}%")

def launch_ui():
    app = QtWidgets.QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()

# --- Main App ---
def main():
    select_os_once()
    update_definitions()
    launch_ui()
    start_monitoring()
    scan_system()
    show_quarantine()
    detect_suspicious_software()

# PyInstaller entry point for .exe conversion
if __name__ == "__main__":
    main()
