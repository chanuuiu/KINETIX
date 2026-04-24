#!/usr/bin/python3

# =========================================
# IMPORTS & GLOBAL CONSTANTS
# =========================================
import os
import sys
import time
import json
import shutil
import socket
import subprocess
import re
import textwrap
from datetime import datetime

# Colors (Hex #ff0029 and Light Green)
RED = '\033[38;2;255;0;41m'
WHITE = '\033[38;5;255m'
BOLD = '\033[1m'
RESET = '\033[0m'
GREEN = '\033[38;2;144;238;144m'
YELLOW = '\033[38;5;226m'
BLUE = '\033[38;5;39m'
CYAN = '\033[38;5;51m'

# Paths & Constants
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
FONT_FILE = os.path.join(SCRIPT_DIR, "ansi_shadow.flf")
VERSION_FILE = os.path.join(SCRIPT_DIR, "version.json")
DICT_FILE = os.path.join(SCRIPT_DIR, "dictionary.json")
SFS_ROOT = "/sdcard/Android/media/com.StefMorojna.SpaceflightSimulator/Mods/Custom_Assets/Texture Packs"

# =========================================
# LOGGING SYSTEM
# =========================================
# Administrative Logging Protocol with Strict Word Wrapping
def sys_log(msg, path="/root", level="info"):
    prefix = f"{GREEN}●{RESET}" if level == "info" else f"{RED}●{RESET}"
    delim = f"{GREEN}»{RESET}"
    raw_base = f"  {prefix} kinetix@core: {path} {delim} "
    box_w = shutil.get_terminal_size().columns
    
    vis_base_len = len(re.sub(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])', '', raw_base))
    
    lines = textwrap.wrap(msg, width=max(20, box_w - vis_base_len))
    if not lines: return
    
    print(f"  {prefix} kinetix@core: {path} {delim} {lines[0]}")
    for line in lines[1:]:
        print(" " * vis_base_len + line)
        
    time.sleep(0.5)

# =========================================
# NETWORK SYSTEM
# =========================================
# Function to check network status
def check_internet():
    try:
        socket.create_connection(("8.8.8.8", 53), timeout=2)
        return True
    except: return False

# =========================================
# SUGGESTION SYSTEM
# =========================================
# Dictionary Suggestion Logic
def suggest_cmd(cmd_input):
    if not os.path.exists(DICT_FILE): return None
    try:
        with open(DICT_FILE, 'r') as f:
            dictionary = json.load(f)
        return dictionary.get(cmd_input.lower(), None)
    except: return None

# =========================================
# SYSTEM CORE
# =========================================
# Function to install dependencies
def setup_dependencies():
    if shutil.which("figlet") is None or not os.path.exists(FONT_FILE):
        os.system('clear')
        sys_log("Preparing KINETIX environment.", level="warning")
        if shutil.which("figlet") is None:
            subprocess.run(["pkg", "install", "figlet", "-y"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        if not os.path.exists(FONT_FILE):
            subprocess.run(["curl", "-s", "-o", FONT_FILE, "https://raw.githubusercontent.com/xero/figlet-fonts/master/ANSI%20Shadow.flf"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        os.system('clear')

# =========================================
# SYSTEM CORE: REFACTORED UPDATE MODULE v1.4.4
# =========================================
def update_kinetix():
    if not check_internet():
        sys_log("Network interface unreachable. Update aborted.", level="error")
        return

    sys_log("Pulling latest repository commits...")
    
    try:
        subprocess.run(["git", "config", "--global", "safe.directory", "*"], capture_output=True)
        
        env = os.environ.copy()
        env["GIT_DISCOVERY_ACROSS_FILESYSTEM"] = "1"

        subprocess.run(
    ["git", "fetch", "origin", "main"],
    cwd=SCRIPT_DIR,
    env=env,
    capture_output=True,
    text=True,
    check=True
)

subprocess.run(
    ["git", "reset", "--hard", "origin/main"],
    cwd=SCRIPT_DIR,
    env=env,
    capture_output=True,
    text=True,
    check=True
)
        
        sys_log("Update applied. Please run ./core.py or python core.py.")
        time.sleep(0.5)

        script_path = os.path.abspath(sys.argv[0])
        os.execv(sys.executable, ['cd', '~', './core.py'] + sys.argv[1:])
        
    except subprocess.CalledProcessError as e:
        sys_log(f"Git execution failed: {e.stderr.strip()}", level="error")
    except Exception as e:
        sys_log(f"System error: {str(e)}", level="error")

# Function to verify core files (Self-Healing)
def verify_integrity():
    if not os.path.exists(VERSION_FILE):
        sys_log("Integrity check failed. version.json is missing.", level="error")
        sys_log("Initiating auto-repair protocol...")
        try:
            subprocess.run(["git", "checkout", "version.json"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except: pass
        update_kinetix()
# =========================================
# UI SYSTEM
# =========================================
# Function to draw the interface
def draw_ui():
    w = shutil.get_terminal_size().columns
    os.system('clear')

    # Banner
    print(f"{RED}┌" + "─"*(w-2) + f"┐{RESET}")
    print(f"  {WHITE}SFS Automated Texture Manager{RESET}")
    print("")
    try:
        logo = subprocess.check_output(["figlet", "-c", "-w", str(w), "-f", FONT_FILE, "KINETIX"]).decode()
        print(f"{RED}{BOLD}{logo}{RESET}", end="")
    except:
        print(f"\n{RED}{BOLD}" + "KINETIX".center(w) + f"{RESET}\n")
    print(f"{RED}└" + "─"*(w-2) + f"┘{RESET}")

    # Patch Notes from JSON
    ver, logs = "?.?.?", ["Dictionary is missing."]
    try:
        with open(VERSION_FILE, 'r') as f:
            data = json.load(f)
            ver = data.get("version", ver)
            logs = data.get("updates", logs)
    except: pass

    status_word = "Connected to internet" if check_internet() else "Offline (Local mode)"

    # Executive Status Routing
    print(f"\n  {GREEN}●{RESET} {WHITE}{status_word}{RESET}")
    print(f"  {GREEN}●{RESET} {WHITE}Logged in as user: root{RESET}\n")

    # Dynamic Version Alignment
    header_left = f"  {RED}CORE UPDATES:{RESET}"
    header_right = f"VERSION: {ver}  "
    vis_left = len(re.sub(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])', '', header_left))
    vis_right = len(re.sub(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])', '', header_right))
    pad = max(1, w - (vis_left + vis_right))

    print(f"{header_left}{' ' * pad}{CYAN}{header_right}{RESET}")
    for log in logs: print(f"  {GREEN}»{RESET} {WHITE}{log}{RESET}")

# Display Help Menu
def show_help():
    draw_ui()
    print(f"  {CYAN}┌─────────────────────────────────────┐{RESET}")
    print(f"  {CYAN}│{RESET} {BOLD}  KINETIX COMMAND REFERENCE {RESET}       {CYAN}│{RESET}")
    print(f"  {CYAN}└─────────────────────────────────────┘{RESET}\n")
    print(f"  {WHITE}?create{RESET}  - Initialize a new project directory tree")
    print(f"  {WHITE}?update{RESET}  - Fetch the latest core updates via Git")
    print(f"  {WHITE}?help{RESET}    - Display administrative options")
    print(f"  {WHITE}?exit{RESET}    - Terminate current shell session")
    print(f"  {WHITE}1-99{RESET}     - Assign target project ID\n")
    
    get_boxed_input(f"{WHITE}Acknowledge input to return{RESET}")

# Unified Flawless ANSI Box Input Helper
def get_boxed_input(prompt_str):
    box_w = min(shutil.get_terminal_size().columns - 2, 70)
    
    ts = datetime.now().strftime('%H:%M:%S')
    full_prompt = f"[{ts}] {prompt_str}"
    
    # Strip ANSI for calculation
    clean_prompt = re.sub(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])', '', full_prompt)
    raw_len = len(clean_prompt)

    print(f"  {RED}┌" + "─"*(box_w-2) + f"┐{RESET}")

    if raw_len > box_w - 4:
        lines = textwrap.wrap(clean_prompt, width=box_w-4)
        for line in lines:
            pad = max(0, box_w - 3 - len(line))
            print(f"  {RED}│{RESET} {WHITE}{line}{RESET}" + " "*pad + f"{RED}│{RESET}")
    else:
        pad1 = max(0, box_w - 3 - raw_len)
        print(f"  {RED}│{RESET} {full_prompt}" + " "*pad1 + f"{RED}│{RESET}")

    print(f"  {RED}│{RESET} {GREEN}»{RESET} " + " "*(box_w-5) + f"{RED}│{RESET}")
    print(f"  {RED}└" + "─"*(box_w-2) + f"┘{RESET}")

    res = input(f"\033[2A\033[7G{WHITE}").strip()
    print("\033[1B", end="")
    return res

# =========================================
# SFS FILE SYSTEM
# =========================================
# Function to navigate SFS files
def navigate():
    if not os.path.exists("/sdcard"):
        os.system("termux-setup-storage")
        time.sleep(0.5)
    if not os.path.exists(SFS_ROOT):
        draw_ui()
        sys_log(f"Critical path not found: {SFS_ROOT}", level="error")
        sys.exit()
    os.chdir(SFS_ROOT)

def get_packs():
    try: return [f for f in os.listdir('.') if os.path.isdir(f)]
    except: return []

# =========================================
# PROJECT MANAGEMENT
# =========================================
# Function to initialize a brand new Project/Pack
def init_new_project():
    draw_ui()
    print(f"  {CYAN}┌─────────────────────────────────────┐{RESET}")
    print(f"  {CYAN}│{RESET} {BOLD}  PROJECT INITIALIZATION PROTOCOL {RESET} {CYAN}│{RESET}")
    print(f"  {CYAN}└─────────────────────────────────────┘{RESET}\n")

    folder_name = get_boxed_input(f"{WHITE}Assign Directory Name{RESET}")
    if not folder_name: return

    proj_path = os.path.join(os.getcwd(), folder_name)
    if os.path.exists(proj_path):
        print("")
        sys_log(f"Namespace conflict. Directory '{folder_name}' already allocated.", path=proj_path, level="error")
        return

    print("")
    sys_log("Awaiting metadata. Empty variables will default.", path=proj_path)
    disp_name = get_boxed_input(f"{WHITE}Display Name [{folder_name}]{RESET}") or folder_name
    version = get_boxed_input(f"{WHITE}Version [1.0]{RESET}") or "1.0"
    desc = get_boxed_input(f"{WHITE}Description{RESET}") or "Custom textures generated with KINETIX Core"
    author = get_boxed_input(f"{WHITE}Author [root]{RESET}") or "root"

    folders = ["Color Textures", "Shape Textures", "Shadow Textures", "Textures"]
    for f in folders:
        os.makedirs(os.path.join(proj_path, f), exist_ok=True)
    time.sleep(0.2)

    pack_info = {
        "DisplayName": disp_name, "Version": version, "Description": desc,
        "Author": author, "ShowIcon": False, "Icon": None, "name": disp_name, "hideFlags": 0
    }

    with open(os.path.join(proj_path, "pack_info.txt"), 'w') as f:
        json.dump(pack_info, f, indent=2)
    time.sleep(0.2)

    print("")
    sys_log(f"Project namespace '{folder_name}' allocated.", path=proj_path)
    sys_log("File structure synchronized. pack_info.txt generated.", path=proj_path)

# =========================================
# VALIDATION ENGINE
# =========================================
# Advanced Feature: JSON Validation
def validate_project(pack_path):
    draw_ui()
    config_dir = os.path.join(pack_path, "Color Textures")
    sys_log("Commencing JSON integrity validation...", path=f"/root/{pack_path}")
    print("")
    
    if not os.path.exists(config_dir):
        sys_log("Config directory missing.", path=f"/root/{pack_path}", level="error")
        return
        
    files = [f for f in os.listdir(config_dir) if f.endswith(".txt")]
    if not files:
        sys_log("Zero configurations found. Validation aborted.", path=f"/root/{pack_path}", level="warning")
        return
        
    errors = 0
    for file in files:
        target = os.path.join(config_dir, file)
        time.sleep(0.2) 
        try:
            with open(target, 'r') as f:
                json.load(f)
            print(f"  {GREEN}●{RESET} {file} {GREEN}»{RESET} Syntax verified")
        except json.JSONDecodeError:
            print(f"  {RED}●{RESET} {file} {RED}»{RESET} Syntax Error")
            errors += 1
            
    print("")
    if errors > 0:
        sys_log(f"Validation complete. {errors} syntax anomalies detected.", path=f"/root/{pack_path}", level="error")
    else:
        sys_log("Validation complete. All components operating optimally.", path=f"/root/{pack_path}")
        
    get_boxed_input(f"{WHITE}Acknowledge output to return{RESET}")

# =========================================
# CONFIG ENGINE
# =========================================
# Config Manager (Batch / Edit / Delete)
def manage_config(pack_path, mode):
    draw_ui()
    config_dir = os.path.join(pack_path, "Color Textures")
    tex_dir = os.path.join(pack_path, "Textures")
    os.makedirs(config_dir, exist_ok=True)
    os.makedirs(tex_dir, exist_ok=True)
    time.sleep(0.2)

    if mode == "create":
        img_name = get_boxed_input(f"{WHITE}Target Texture (exclude .png){RESET}")
        conf_name = get_boxed_input(f"{WHITE}Designate Output File{RESET}")
        bp_name = get_boxed_input(f"{WHITE}Assign BP Name{RESET}")

        data = {
            "colorTex": {
                "textures": [{"texture": f"{img_name}.png", "ideal": 0.0}],
                "center": {"mode": "Stretch", "sizeMode": "Aspect", "size": 0.5, "logoHeightPercent": 0.5, "scaleLogoToFit": False},
                "border_Bottom": {"uvSize": 0.0, "sizeMode": "Aspect", "size": 0.5},
                "border_Top": {"uvSize": 0.0, "sizeMode": "Aspect", "size": 0.5},
                "fixedWidth": False, "fixedWidthValue": 1.0, "flipToLight_X": False, "flipToLight_Y": False, "metalTexture": False, "icon": None
            },
            "tags": ["tank", "cone", "fairing"], "name": bp_name, "hideFlags": "None"
        }
        with open(os.path.join(config_dir, f"{conf_name}.txt"), 'w') as f:
            json.dump(data, f, indent=2)
        time.sleep(0.2)
        print("")
        sys_log(f"Configuration matrix {conf_name}.txt compiled and written to disk.", path=f"/root/{pack_path}")

    elif mode == "batch":
        images = [f for f in os.listdir(tex_dir) if f.endswith(".png")]
        if not images:
            print("")
            sys_log(f"Target directory '{tex_dir}' contains zero valid textures.", path=f"/root/{pack_path}", level="error")
            return

        print("")
        sys_log(f"Batch execution engaged. Queue size: {len(images)}", path=f"/root/{pack_path}")
        print("")
        for img in images:
            name = img.replace(".png", "")
            data = {
                "colorTex": {
                    "textures": [{"texture": img, "ideal": 0.0}],
                    "center": {"mode": "Stretch", "sizeMode": "Aspect", "size": 0.5, "logoHeightPercent": 0.5, "scaleLogoToFit": False},
                    "border_Bottom": {"uvSize": 0.0, "sizeMode": "Aspect", "size": 0.5},
                    "border_Top": {"uvSize": 0.0, "sizeMode": "Aspect", "size": 0.5},
                    "fixedWidth": False, "fixedWidthValue": 1.0, "flipToLight_X": False, "flipToLight_Y": False, "metalTexture": False, "icon": None
                },
                "tags": ["tank", "cone", "fairing"], "name": name, "hideFlags": "None"
            }
            with open(os.path.join(config_dir, f"{name}.txt"), 'w') as f:
                json.dump(data, f, indent=2)
            time.sleep(0.05)
            print(f"  {GREEN}●{RESET} {name}.txt {GREEN}»{RESET} Payload generated")

        print("")
        sys_log("Batch operations complete. Engine suspended.", path=f"/root/{pack_path}")

    elif mode in ["edit", "delete"]:
        files = [f for f in os.listdir(config_dir) if f.endswith(".txt")]
        if not files: 
            print("")
            sys_log("Directory empty. Operation aborted.", path=f"/root/{pack_path}", level="error")
            return
        for i, f in enumerate(files): print(f"  {RED}[{i+1}]{RESET} {WHITE}{f}{RESET}")

        c = get_boxed_input(f"{WHITE}Target Identifier (0=Cancel){RESET}")
        if c.isdigit() and int(c) != 0:
            target = os.path.join(config_dir, files[int(c)-1])
            if mode == "delete": 
                os.remove(target)
                print("")
                sys_log("Asset purged from directory.", path=f"/root/{pack_path}")
            else:
                new_n = get_boxed_input(f"{WHITE}Update BP Menu string{RESET}")
                with open(target, 'r+') as f:
                    d = json.load(f); d["name"] = new_n
                    f.seek(0); json.dump(d, f, indent=2); f.truncate()
                time.sleep(0.2)
                print("")
                sys_log("Configuration variables updated.", path=f"/root/{pack_path}")

# =========================================
# MAIN LOOP
# =========================================
if __name__ == "__main__":
    setup_dependencies()
    verify_integrity()
    navigate()

    while True:
        draw_ui()
        packs = get_packs()

        print(f"\n  {WHITE}ACTIVE WORKSPACES:{RESET}")
        if packs:
            for i, p in enumerate(packs):
                print(f"  {CYAN}[{i+1}]{RESET} {WHITE}{p}{RESET}")
        else:
            print(f"  {RED}●{RESET} No directories allocated.")

        print(f"\n  {BOLD}?exit{RESET} Terminate · {BOLD}?create{RESET} Scaffold Project · {BOLD}?update{RESET} Sync Core")
        print(f"  {BOLD}?help{RESET} Directives\n")
        path_disp = f"{GREEN}●{RESET} {WHITE}kinetix@core: /root{RESET}"
        raw_cmd = get_boxed_input(path_disp)

        if not raw_cmd: continue

        if raw_cmd.lower() in ['?exit', '?stop', 'exit', 'quit', '0']: break
        elif raw_cmd.lower() == '?update': update_kinetix(); continue
        elif raw_cmd.lower() == '?create': init_new_project(); continue
        elif raw_cmd.lower() == '?help': show_help(); continue

        if raw_cmd.isdigit() and 1 <= int(raw_cmd) <= len(packs):
            p_name = packs[int(raw_cmd)-1]
            while True:
                draw_ui()
                print(f"  {WHITE}MOUNTED TARGET:{RESET} {CYAN}{p_name}{RESET}\n")

                print(f"  {WHITE}[1]{RESET} Generate Configuration")
                print(f"  {WHITE}[2]{RESET} Modify Configuration")
                print(f"  {WHITE}[3]{RESET} Purge Configuration")
                print(f"  {WHITE}[4]{RESET} Execute Batch Engine")
                print(f"  {WHITE}[5]{RESET} Validate Project Integrity")
                print(f"  {WHITE}[0]{RESET} Detach Target\n")

                path_disp = f"{GREEN}●{RESET} {WHITE}kinetix@core: /root/{p_name}{RESET}"
                raw_sub = get_boxed_input(path_disp)

                if raw_sub == '1': manage_config(p_name, "create")
                elif raw_sub == '2': manage_config(p_name, "edit")
                elif raw_sub == '3': manage_config(p_name, "delete")
                elif raw_sub == '4': manage_config(p_name, "batch")
                elif raw_sub == '5': validate_project(p_name)
                elif raw_sub == '0': break
                elif raw_sub:
                    suggestion = suggest_cmd(raw_sub)
                    print("")
                    if suggestion:
                        print(f"  {WHITE}[SYSTEM]: Unknown command. Did you mean: \"{suggestion}\"? {GREEN}»{RESET}")
                    else:
                        sys_log(f"Unknown directive encountered: '{raw_sub}'.", path=f"/root/{p_name}", level="error")
                        sys_log("Argument invalid. Execute '?help' for syntax definitions.", path=f"/root/{p_name}", level="error")
                    time.sleep(0.5)
        else:
            suggestion = suggest_cmd(raw_cmd)
            print("")
            if suggestion:
                print(f"  {WHITE}[SYSTEM]: Unknown command. Did you mean: \"{suggestion}\"? {GREEN}»{RESET}")
            else:
                sys_log(f"Unknown directive encountered: '{raw_cmd}'.", level="error")
                sys_log("Argument invalid. Execute '?help' for syntax definitions.", level="error")
            time.sleep(2)
