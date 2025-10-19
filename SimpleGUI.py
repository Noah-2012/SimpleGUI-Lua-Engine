import pygame
import logging
from lupa import LuaRuntime
from SimpleGUIClasses import GUIWindow, GUILabel, GUIButton, GUITextEntry
import SimpleGUIClasses
from SimpleGUICSSParser import *

# Logging Setup
logging.basicConfig(
    level=logging.INFO,
    format='[%(levelname)s] [%(name)s] %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)

# Logger für verschiedene Komponenten
logger = logging.getLogger('SIMPLEGUI')
css_logger = logging.getLogger('CSSPARSER')
lua_logger = logging.getLogger('LUA')

pygame.font.init()

lua_code_callback = """
    local frame = SimpleGUI.Create("Window")
    frame:SetTitle("Lua Callback Window")
    frame:SetSize(500, 500)
    frame:Center()
    frame:SetDraggable(true)
    frame:ShowCloseButton(true)

    local label = SimpleGUI.Create("Label", frame)
    label:SetText("This window was created from a Lua callback!")
    label:Margin(10, 10, 10, 10)

    local link = SimpleGUI.Create("Label", frame)
    link:SetLink("A little Link!", "https://github.com")
    link:Margin(10, 40, 10, 10)

    local button = SimpleGUI.Create("Button", frame)
    button:SetText("Close")
    button:SetSize(100, 30)
    button:Margin(10, 70, 10, 10)
    button.OnClick = function()
        frame:Close()
    end

    local text_entry = SimpleGUI.Create("TextEntry", frame)
    text_entry:SetPlaceholder("Type here...")
    text_entry:SetSize(200, 30)
    text_entry:Margin(10, 110, 10, 10)
    
    local button2 = SimpleGUI.Create("Button", frame)
    button2:SetText("Create new Window")
    button2:SetSize(150, 30)
    button2:Margin(10, 150, 10, 10)
    button2.OnClick = function()
        local new_window_title = text_entry:GetText()
        local new_window = SimpleGUI.Create("Window")
        new_window:SetTitle(new_window_title)
        new_window:SetSize(100, 100)
        new_window:SetPos(math.random(0, 1820), math.random(0, 980))
    end
"""

def ParseCSS(css_code):
    parser = CSSParser()
    parser.parse(css_code)
    css_logger.info("Parse CSS Styles...")

    css_root = parser.get(":root")
    SimpleGUIClasses.GUIWindow.CLOSE_BUTTON_SIZE = px_to_int(css_root.__close_button_size)
    SimpleGUIClasses.GUIWindow.TITLE_BAR_HEIGHT = px_to_int(css_root.__title_bar_height)
    css_logger.info("Loaded CSS Root settings.")

    css_window = parser.get("window")
    SimpleGUIClasses.GUIWindow.bg_color = hex_to_rgb(css_window.background_color)
    SimpleGUIClasses.GUIWindow.title_color = hex_to_rgb(css_window.__title_color)
    SimpleGUIClasses.GUIWindow.text_color = hex_to_rgb(css_window.__text_color)
    SimpleGUIClasses.GUIWindow.border_color = hex_to_rgb(css_window.border_color)
    SimpleGUIClasses.GUIWindow.border_radius = px_to_int(css_window.border_radius)
    SimpleGUIClasses.GUIWindow.border_radius_close_button = px_to_int(css_window.__border_radius_close_button)
    css_logger.info("Loaded CSS Window settings.")

    css_label = parser.get("label")
    SimpleGUIClasses.GUILabel.color = hex_to_rgb(css_label.color)
    SimpleGUIClasses.GUILabel.link_color = hex_to_rgb(css_label.__link_color)
    css_logger.info("Loaded CSS Label settings.")

    css_button = parser.get("button")
    SimpleGUIClasses.GUIButton.bg_color = hex_to_rgb(css_button.background_color)
    SimpleGUIClasses.GUIButton.hover_color = hex_to_rgb(css_button.__hover_color)
    SimpleGUIClasses.GUIButton.text_color = hex_to_rgb(css_button.__text_color)
    css_logger.info("Loaded CSS Button settings.")

    css_textentry = parser.get("textentry")
    SimpleGUIClasses.GUITextEntry.bg_color = hex_to_rgb(css_textentry.background_color)
    SimpleGUIClasses.GUITextEntry.border_color = hex_to_rgb(css_textentry.border_color)
    SimpleGUIClasses.GUITextEntry.active_border_color = hex_to_rgb(css_textentry.__active_border_color)
    SimpleGUIClasses.GUITextEntry.text_color = hex_to_rgb(css_textentry.__text_color)
    SimpleGUIClasses.GUITextEntry.placeholder_color = hex_to_rgb(css_textentry.__placeholder_color)
    css_logger.info("Loaded CSS TextEntry settings.")

def lua_prefix_printer(*args):
    lua_logger.info(' '.join(str(arg) for arg in args))

class SimpleGUI:
    windows = []
    focused_window = None
    last_window = None

    @staticmethod
    def ensure_unique_position(window):
        while any((window.x == w.x and window.y == w.y) for w in SimpleGUI.windows if w != window):
            window.x += 30
            window.y += 30

    @staticmethod
    def Create(kind, parent=None):
        if kind == "Window":
            window = GUIWindow("Untitled", 0, 0, 200, 100)
            SimpleGUI.ensure_unique_position(window)
            SimpleGUI.windows.insert(1, window)
            if SimpleGUI.last_window is not None and SimpleGUI.last_window != window:
                logger.debug("--------------------------------------------------")
            SimpleGUI.last_window = window
            return window
        elif kind == "Label":
            if parent is None:
                raise ValueError("Labels mussen ein Parent-Fenster haben!")
            label = GUILabel(parent)
            parent.children.append(label)
            if SimpleGUI.last_window is not None and SimpleGUI.last_window != parent:
                logger.debug("--------------------------------------------------")
            SimpleGUI.last_window = parent
            label.print_parent(parent=parent)
            return label
        elif kind == "Button":
            if parent is None:
                raise ValueError("Buttons mussen ein Parent-Fenster haben!")
            button = GUIButton(parent)
            parent.children.append(button)
            if SimpleGUI.last_window is not None and SimpleGUI.last_window != parent:
                logger.debug("--------------------------------------------------")
            SimpleGUI.last_window = parent
            button.print_parent(parent=parent)
            return button
        elif kind == "TextEntry":
            if parent is None:
                raise ValueError("TextEntries mussen ein Parent-Fenster haben!")
            text_entry = GUITextEntry(parent)
            parent.children.append(text_entry)
            if SimpleGUI.last_window is not None and SimpleGUI.last_window != parent:
                logger.debug("--------------------------------------------------")
            SimpleGUI.last_window = parent
            text_entry.print_parent(parent=parent)
            return text_entry
        else:
            raise ValueError(f"Unbekannter GUI-Type: {kind}")

debug = SimpleGUIClasses.DebugOverlay()

lua = LuaRuntime(unpack_returned_tuples=True)
lua.globals().SimpleGUI = SimpleGUI
lua.globals()['print'] = lua_prefix_printer

SimpleGUIClasses.debug = debug
SimpleGUIClasses.SimpleGUI = SimpleGUI
SimpleGUIClasses.lua = lua

try:
    with open("style.css", "r", encoding="utf-8") as f:
        css_code = f.read()
    ParseCSS(css_code)
    logger.info("Loaded style.css successfully.")
except Exception as e:
    logger.error(f"Error loading style.css: {e}")

logger.info("Initialized Lua Runtime and SimpleGUI bindings.")

try:
    with open ("script.lua", "r", encoding="utf-8") as f:
        lua_code = f.read()

    lua.execute(lua_code)
except Exception as e:
    logger.error(f"Error loading script.lua: {e}")
    logger.info("Press F3 for debug log or press F5 to run Callback script.")

logger.debug("--------------------------------------------------")
logger.info("Starting main loop...")

pygame.init()
screen = pygame.display.set_mode((1920, 1080), pygame.FULLSCREEN)
font = pygame.font.SysFont("Verdana", 13)
clock = pygame.time.Clock()
vhs_menu = SimpleGUIClasses.VHSMenu()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            running = False

        if event.type == pygame.KEYDOWN and event.key == pygame.K_F2:
            vhs_menu.toggle_menu()

        if event.type == pygame.KEYDOWN and event.key == pygame.K_F3 and not (pygame.key.get_mods() & pygame.KMOD_SHIFT):
            debug.toggle_log()

        if event.type == pygame.KEYDOWN and event.key == pygame.K_F3 and (pygame.key.get_mods() & pygame.KMOD_SHIFT):
            debug.messages.clear()

        if event.type == pygame.KEYDOWN and event.key == pygame.K_F4 and not (pygame.key.get_mods() & pygame.KMOD_SHIFT):
            if SimpleGUI.windows:
                SimpleGUI.windows[0].debug_mode_adva = False
                SimpleGUI.windows[0].toggle_debug()

        if event.type == pygame.KEYDOWN and event.key == pygame.K_F4 and (pygame.key.get_mods() & pygame.KMOD_SHIFT):
            if SimpleGUI.windows:
                SimpleGUI.windows[0].toggle_debug_advanced()

        if event.type == pygame.KEYDOWN and event.key == pygame.K_F5:
            lua.execute(lua_code_callback)

        if vhs_menu.active:
            if vhs_menu.handle_event(event):
                continue

        for win in SimpleGUI.windows:
            if win.handle_event(event):
                break

    screen.fill((20, 20, 20))

    vhs_menu.last_fps = clock.get_fps()
    
    for win in reversed(SimpleGUI.windows):
        win.draw(screen, font)

        if win is not SimpleGUI.windows[0]:
            dark_surface = pygame.Surface((win.width, win.height), pygame.SRCALPHA)
            dark_surface.fill((0, 0, 0, 50))
            screen.blit(dark_surface, (win.x, win.y))

    vhs_menu.draw(screen)
    debug.draw(screen)

    pygame.display.flip()
    clock.tick(1000)

pygame.quit()