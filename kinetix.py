import os
import shutil
import subprocess
import json
import sys
import time

# --- CONFIG & THEME ---
RED = '\033[38;2;255;0;41m' 
WHITE = '\033[38;5;255m'
BOLD = '\033[1m'
RESET = '\033[0m'
GREEN = '\033[1;32m'
YELLOW = '\033[1;33m'
BLUE = '\033[1;34m'

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
FONT_FILE = os.path.join(SCRIPT_DIR, "ansi_shadow.flf")
SFS_ROOT = "/sdcard/Android/media/com.StefMorojna.SpaceflightSimulator/Mods/Custom_Assets/Texture Packs"

def setup_dependencies():
    if shutil.which("figlet") is None or not os.path.exists(FONT_FILE):
        os.system('clear')
        print(f"{YELLOW}Downloading required packages via pkg.{RESET}")
        
        if shutil.which("figlet") is None:
            subprocess.run(["pkg", "install", "figlet", "-y"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        time.sleep(2)
        print(f"{GREEN}Extracting downloaded dependencies...{RESET}")
        
        if not os.path.exists(FONT_FILE):
            subprocess.run(["curl", "-s", "-o", FONT_FILE, "https://raw.githubusercontent.com/xero/figlet-fonts/master/ANSI%20Shadow.flf"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        time.sleep(2)
        os.system('clear')

setup_dependencies()

# --- TERMINAL UI ---
def draw_ui():
    w = shutil.get_terminal_size().columns
    os.system('clear')
    
    # Top Border
    print(f"{RED}┌" + "─"*(w-2) + f"┐{RESET}")
    print(f"  {GREEN} An SFS Automated Texture Manager{RESET}")
    print("")
    # Centered Native Figlet Logo
    try:
        logo = subprocess.check_output(["figlet", "-c", "-w", str(w), "-f", FONT_FILE, "KINETIX"]).decode()
        print(f"{RED}{BOLD}{logo}{RESET}", end="")
    except: 
        print(f"\n{RED}{BOLD}" + "KINETIX".center(w) + f"{RESET}\n")
        
    # Bottom Border
    print(f"{RED}└" + "─"*(w-2) + f"┘{RESET}")
    
    # Right-Aligned Status (Calculating visible length without ANSI codes)
    visible_info = "● Status: ONLINE"
    padding = w - len(visible_info) - 1
    if padding < 0: padding = 0
    print(f"{' '*padding}{WHITE}● Status: {GREEN}ONLINE{RESET}")
    
    # Socials
    print(f"  {RED}SOCIALS")
    print(f"  {GREEN}GitHub:  https://github.com/chanuuiu{RESET}")
    print(f"  {BLUE}Discord: _chanuuu(chanu){RESET}")
    print(f"  {YELLOW}Forums: chano \n")

def navigate():
    if not os.path.exists("/sdcard"):
        os.system("termux-setup-storage")
        time.sleep(2)
    try:
        if not os.path.exists(SFS_ROOT):
            draw_ui()
            print(f"{RED}[!] PATH ERROR: Directory not found.{RESET}")
            print(f"{YELLOW}Path:{RESET} {SFS_ROOT}")
            sys.exit()
        os.chdir(SFS_ROOT)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit()

def get_packs():
    try:
        return [f for f in os.listdir('.') if os.path.isdir(f)]
    except:
        return []

def manage_config(pack_path, mode):
    draw_ui()
    config_dir = os.path.join(pack_path, "Color Textures")
    tex_dir = os.path.join(pack_path, "Textures")
    os.makedirs(config_dir, exist_ok=True)
    os.makedirs(tex_dir, exist_ok=True)

    if mode == "create":
        print(f"  {YELLOW}Scanning Textures...{RESET}")
        try:
            images = [f for f in os.listdir(tex_dir) if f.endswith(".png")]
            if images:
                for img in images: print(f"  {RED}»{RESET} {WHITE}{img}{RESET}")
            else:
                print(f"  {RED}[!] No .png images found in {tex_dir}{RESET}")
        except: pass
        
        conf_name = input(f"\n  {BOLD}Config Filename:{RESET} ").strip()
        img_name = input(f"  {BOLD}Texture Name (no .png):{RESET} ").strip()
        bp_name = input(f"  {BOLD}BP Menu Name:{RESET} ").strip()

        data = {
            "colorTex": {
                "textures": [{"texture": f"{img_name}.png", "ideal": 0.0}],
                "center": {"mode": "Stretch", "sizeMode": "Aspect", "size": 0.5, "logoHeightPercent": 0.5, "scaleLogoToFit": False},
                "border_Bottom": {"uvSize": 0.0, "sizeMode": "Aspect", "size": 0.5},
                "border_Top": {"uvSize": 0.0, "sizeMode": "Aspect", "size": 0.5},
                "fixedWidth": False, "fixedWidthValue": 1.0, "flipToLight_X": False, "flipToLight_Y": False, "metalTexture": False, "icon": None
            },
            "tags": ["tank", "cone", "fairing"],
            "pack_Redstone_Atlas": False, "multiple": False, "segments": [],
            "name": bp_name, "hideFlags": "None"
        }
        with open(os.path.join(config_dir, f"{conf_name}.txt"), 'w') as f:
            json.dump(data, f, indent=2)
        print(f"\n  {GREEN}SUCCESS: Config generated!{RESET}")
        time.sleep(1)

    elif mode in ["edit", "delete"]:
        files = [f for f in os.listdir(config_dir) if f.endswith(".txt")]
        if not files: 
            print(f"  {RED}EMPTY: No configs found.{RESET}")
            time.sleep(1); return
        
        for i, f in enumerate(files): print(f"  [{RED}{i+1}{RESET}] {WHITE}{f}{RESET}")
        choice = input(f"\n  {BOLD}Select ID to {mode} (0 to cancel):{RESET} ")
        if not choice.isdigit() or int(choice) == 0: return
        
        idx = int(choice) - 1
        target = os.path.join(config_dir, files[idx])
        if mode == "delete":
            os.remove(target)
            print(f"  {RED}DELETED: {files[idx]}{RESET}")
        else:
            new_bp = input(f"  {YELLOW}New BP Name:{RESET} ")
            with open(target, 'r+') as f:
                d = json.load(f)
                d["name"] = new_bp
                f.seek(0); json.dump(d, f, indent=2); f.truncate()
            print(f"  {GREEN}UPDATED!{RESET}")
        time.sleep(1)

if __name__ == "__main__":
    navigate()
    while True:
        draw_ui()
        packs = get_packs()
        print(f"  {GREEN}ACTIVE PROJECTS:{RESET}")
        for i, p in enumerate(packs): 
            print(f"  {YELLOW}ID:{i+1}{RESET} | {WHITE}{p}{RESET}")
        
        print(f"  {RED}[0] EXIT{RESET}")
        
        cmd = input(f"\n{WHITE}~/sfs/texture-manager{RESET}\n{RED}❯ {RESET}{WHITE}").strip()
        
        if cmd == '0' or cmd == '?stop': 
            os.system('clear')
            print(f"{RED}Terminating session...{RESET}")
            break
        if cmd.isdigit() and 1 <= int(cmd) <= len(packs):
            p_name = packs[int(cmd)-1]
            while True:
                draw_ui()
                print(f"  SELECTED: {GREEN}{p_name}{RESET}\n")
                print(f"  [{RED}1{RESET}] {WHITE}Create{RESET}   [{RED}2{RESET}] {WHITE}Edit{RESET}   [{RED}3{RESET}] {WHITE}Delete{RESET}   [{RED}0{RESET}] {WHITE}Return{RESET}")
                
                sub = input(f"\n{WHITE}~/sfs/texture-manager/{p_name}{RESET}\n{RED}❯ {RESET}{WHITE}").strip()
                if sub == '1': manage_config(p_name, "create")
                elif sub == '2': manage_config(p_name, "edit")
                elif sub == '3': manage_config(p_name, "delete")
                elif sub == '0': break

