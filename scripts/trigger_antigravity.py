"""
Antigravity RPA Trigger Script — Image Matching Mode
Finds "Ask anything" input box by image matching, clicks it, pastes message, sends.

Usage: python trigger_antigravity.py "Your message here"
"""

import asyncio
import sys
import os
import ctypes
import pyautogui
import pyperclip
from PIL import Image, ImageDraw, ImageFont

pyautogui.FAILSAFE = False

AUTOMATION_DIR = r'D:\Gemini\agent-hand\openclaw-automation'
sys.path.insert(0, AUTOMATION_DIR)
os.chdir(AUTOMATION_DIR)

from app.core.automation import AutomationEngine

# Fix DPI
try:
    ctypes.windll.shcore.SetProcessDpiAwareness(2)
except Exception:
    try:
        ctypes.windll.user32.SetProcessDPIAware()
    except Exception:
        pass

TEMPLATE_PATH = os.path.join(r'D:\Gemini\agent-hand\bridge\scripts', 'ask_anything_template.png')


def ensure_template():
    """Generate a template image of 'Ask anything' text for matching."""
    if os.path.exists(TEMPLATE_PATH):
        return
    # Render the text with approximate IDE styling
    img = Image.new('RGB', (120, 22), color=(228, 223, 212))
    draw = ImageDraw.Draw(img)
    try:
        font = ImageFont.truetype("segoeui.ttf", 13)
    except Exception:
        font = ImageFont.load_default()
    draw.text((5, 3), "Ask anything", fill=(140, 135, 128), font=font)
    img.save(TEMPLATE_PATH)
    print(f"[i] Template generated: {TEMPLATE_PATH}")


async def trigger_antigravity(message: str):
    print("=" * 50)
    print("  Antigravity RPA Trigger (Image Match)")
    print("=" * 50)

    engine = AutomationEngine(human_like=True)
    ensure_template()

    # Step 1: Clipboard
    print("[1/4] Clipboard ready.")
    pyperclip.copy(message)

    # Step 2: Focus window
    print("[2/4] Focusing Antigravity...")
    if not await engine.focus_window("Antigravity"):
        print("[x] Cannot find Antigravity window!")
        return False
    print("[v] Focused.")
    await asyncio.sleep(1.0)

    # Step 3: Find "Ask anything" by image match
    print("[3/4] Searching for 'Ask anything' input...")
    
    found = False
    # Try multiple confidence levels
    for conf in [0.7, 0.6, 0.5]:
        try:
            loc = pyautogui.locateOnScreen(TEMPLATE_PATH, confidence=conf)
            if loc:
                cx, cy = pyautogui.center(loc)
                print(f"      [v] Found at ({cx}, {cy}) confidence={conf}")
                pyautogui.moveTo(cx, cy, duration=0.3)
                await asyncio.sleep(0.2)
                pyautogui.click()
                found = True
                break
        except Exception as e:
            print(f"      [!] conf={conf}: {e}")

    if not found:
        print("      [!] Image match failed. Taking screenshot for debug...")
        debug_path = os.path.join(r'D:\Gemini\agent-hand\bridge\scripts', 'debug_screenshot.png')
        pyautogui.screenshot(debug_path)
        print(f"      Saved: {debug_path}")
        print("      Falling back to coordinate click...")
        
        # Coordinate fallback
        user32 = ctypes.windll.user32
        import ctypes.wintypes
        
        def find_window():
            results = []
            def cb(hwnd, _):
                if user32.IsWindowVisible(hwnd):
                    buf = ctypes.create_unicode_buffer(256)
                    user32.GetWindowTextW(hwnd, buf, 256)
                    if 'antigravity' in buf.value.lower():
                        r = ctypes.wintypes.RECT()
                        user32.GetWindowRect(hwnd, ctypes.byref(r))
                        results.append((r.left, r.top, r.right, r.bottom))
                return True
            WNDENUMPROC = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.wintypes.HWND, ctypes.wintypes.LPARAM)
            user32.EnumWindows(WNDENUMPROC(cb), 0)
            return results
        
        rects = find_window()
        if rects:
            left, top, right, bottom = rects[0]
            cx = left + (right - left) // 2
            cy = bottom - 120
            print(f"      Clicking ({cx}, {cy})...")
            pyautogui.moveTo(cx, cy, duration=0.3)
            pyautogui.click()
        else:
            print("[x] No window found!")
            return False

    await asyncio.sleep(0.5)

    # Step 4: Paste and send
    print("[4/4] Pasting and sending...")
    pyautogui.hotkey('ctrl', 'a')
    await asyncio.sleep(0.1)
    pyautogui.hotkey('ctrl', 'v')
    await asyncio.sleep(0.3)
    pyautogui.press('enter')

    print("[v] Message sent!")
    return True


if __name__ == "__main__":
    msg = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else \
        "Bridge上有新的任务，请检查 workspace/antigravity_tasks 目录并开始处理。"
    try:
        success = asyncio.run(trigger_antigravity(msg))
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        sys.exit(1)
