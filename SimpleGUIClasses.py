from tkinter import SE
import pygame
import webbrowser
import math

debug = None
SimpleGUI = None
lua = None

pygame.init()

pygame.key.set_repeat(300, 30)

class GUIWindow:
    TITLE_BAR_HEIGHT = 24
    CLOSE_BUTTON_SIZE = 20

    bg_color = (40, 40, 40)
    title_color = (60, 60, 60)
    text_color = (255, 255, 255)
    border_color = (60, 60, 60)
    border_radius = 4
    border_radius_close_button = 2

    def __init__(self, title, x, y, w, h):
        self.title = title
        self.x = x
        self.y = y
        self.width = w
        self.height = h
        self.visible = True
        self.bg_color = self.__class__.bg_color
        self.title_color = self.__class__.title_color
        self.text_color = self.__class__.text_color
        self.border_color = self.__class__.border_color
        self.border_radius = self.__class__.border_radius
        self.border_radius_close_button = self.__class__.border_radius_close_button
        self.draggable = False
        self.dragging = False
        self.drag_offset = (0, 0)
        self.show_close = False
        self.close_hover = False
        self.children = []
        self.debug_mode = False
        self.debug_mode_adva = False

    def SetTitle(self, title):
        self.title = title
        print(f"[GUIWINDOW] Titel gesetzt: {title}")
        debug.log(f"Created Window: {title}")

    def SetSize(self, w, h):
        self.width, self.height = w, h
        print(f"[GUIWINDOW] Grosse geandert: {w}x{h}")

    def SetPos(self, x, y):
        self.x, self.y = x, y
        print(f"[GUIWINDOW] Position geandert: ({x}, {y})")

    def SetBackgroundColor(self, r, g, b):
        self.bg_color = r, g, b
        print(f"[GUIWINDOW] Hintergrundfarbe geandert: ({r}, {g}, {b})")

    def Center(self):
        self.x = (1920 - self.width) / 2
        self.y = (1080 - self.height) / 2
        print("[GUIWINDOW] Fenster zentriert")

    def ShowCloseButton(self, show):
        self.show_close = bool(show)

    def SetDraggable(self, state):
        self.draggable = bool(state)
        print("[GUIWINDOW] Dragging aktiviert")

    def Close(self):
        if self in SimpleGUI.windows:
            SimpleGUI.windows.remove(self)
        debug.log(f"[GUIWINDOW] Closed Window: {self.title}")

    def toggle_debug(self):
        self.debug_mode = not self.debug_mode
        print(f"[GUIWINDOW] Debug Mode {'aktiviert' if self.debug_mode else 'deaktiviert'} fuer Fenster: {self.title}")
        debug.log(f"Debug Mode {'aktiviert' if self.debug_mode else 'deaktiviert'} fuer Fenster: {self.title}")

    def toggle_debug_advanced(self):
        self.debug_mode = not self.debug_mode
        self.debug_mode_adva = not self.debug_mode_adva
        print(f"[GUIWINDOW] Debug Mode {'aktiviert' if self.debug_mode else 'deaktiviert'} fuer Fenster: {self.title}")
        debug.log(f"Debug Mode {'aktiviert' if self.debug_mode else 'deaktiviert'} fuer Fenster: {self.title}")

    def handle_event(self, event):
        mx, my = None, None
        if event.type == pygame.MOUSEMOTION:
            mx, my = event.pos

            if self.show_close:
                btn_rect = pygame.Rect(self.x + self.width - self.CLOSE_BUTTON_SIZE - 4,
                                       self.y + 2,
                                       self.CLOSE_BUTTON_SIZE,
                                       self.CLOSE_BUTTON_SIZE)
                self.close_hover = btn_rect.collidepoint(mx, my)

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mx, my = event.pos

            if self.show_close:
                btn_rect = pygame.Rect(self.x + self.width - self.CLOSE_BUTTON_SIZE - 4, 
                                       self.y + 2,
                                       self.CLOSE_BUTTON_SIZE,
                                       self.CLOSE_BUTTON_SIZE)
                if btn_rect.collidepoint(mx, my):
                    if self in SimpleGUI.windows:
                        SimpleGUI.windows.remove(self)
                    return True

            for child in reversed(self.children):
                if hasattr(child, "handle_event"):
                    if child.handle_event(event):
                        return True

            if (self.x <= mx <= self.x + self.width) and (self.y <= my <= self.y + self.TITLE_BAR_HEIGHT):
                if self.draggable:
                    self.dragging = True
                    self.drag_offset = (mx - self.x, my - self.y)

                if self != SimpleGUI.windows[0]:
                    SimpleGUI.windows.remove(self)
                    SimpleGUI.windows.insert(0, self)

                return True

            return False

        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.dragging = False

        elif event.type == pygame.MOUSEMOTION and self.dragging:
            mx, my = event.pos
            self.x = mx - self.drag_offset[0]
            self.y = my - self.drag_offset[1]

        for child in reversed(self.children):
            if hasattr(child, "handle_event"):
                child.handle_event(event)


    def draw(self, screen, font):
        if not self.visible:
            return

        border_radius = self.border_radius
        border_radius_close = self.border_radius_close_button
        # Fenster
        pygame.draw.rect(screen, self.bg_color, (self.x, self.y + self.TITLE_BAR_HEIGHT, self.width, self.height - self.TITLE_BAR_HEIGHT), border_bottom_left_radius=border_radius, border_bottom_right_radius=border_radius)
        # Titelleiste
        pygame.draw.rect(screen, self.title_color, (self.x, self.y, self.width, self.TITLE_BAR_HEIGHT), border_top_right_radius=border_radius, border_top_left_radius=border_radius)
        # Fenster-Outline
        pygame.draw.rect(screen, self.border_color, (self.x, self.y, self.width, self.height), width=1, border_radius=border_radius)
        
        # Titeltext
        text = font.render(self.title, True, self.text_color)
        screen.blit(text, (self.x + 10, self.y + 4))

        # Closebutton
        if self.show_close:
            btn_rect = pygame.Rect(self.x + self.width - self.CLOSE_BUTTON_SIZE - 4, 
                                   self.y + 2,
                                   self.CLOSE_BUTTON_SIZE,
                                   self.CLOSE_BUTTON_SIZE)
            color = (200, 50, 50) if self.close_hover else (100, 100, 100)
            pygame.draw.rect(screen, color, btn_rect, border_radius=border_radius_close)

            line_color = (255, 255, 255)
            line_width = 2

            cx = btn_rect.centerx - 1
            cy = btn_rect.centery

            size = self.CLOSE_BUTTON_SIZE // 2 - 3

            pygame.draw.line(
                screen,
                line_color,
                (cx - size // 2, cy - size // 2),
                (cx + size // 2, cy + size // 2),
                line_width
            )
            pygame.draw.line(
                screen,
                line_color,
                (cx - size // 2, cy + size // 2),
                (cx + size // 2, cy - size // 2),
                line_width
            )

        if self.debug_mode:
            screen_width = screen.get_width()
            screen_height = screen.get_height()

            pygame.draw.line(screen, (255, 0, 0), (0, self.y), (screen_width, self.y), 1)

            y_text = font.render(f"Y: {int(self.y)}px", True, (255, 0, 0))
            screen.blit(y_text, (10, self.y + 5))

            pygame.draw.line(screen, (0, 255, 0), (self.x, 0), (self.x, screen_height), 1)

            x_text = font.render(f"X: {int(self.x)}px", True, (0, 255, 0))
            screen.blit(x_text, (self.x + 5, 10))

            info_x = self.x + self.width + 10
            info_y = self.y + 10
            info_texts = [
                f"Name: {self.title}",
                f"Width: {int(self.width)}px",
                f"Height: {int(self.height)}px",
                f"Children: {len(self.children)}",
                f"Pos: X: {int(self.x)}px, Y: {int(self.y)}px"
            ]

            if self.debug_mode_adva:
                info_attr = [f"{key}: {value}" for key, value in self.__dict__.items() if key not in ["children", "font"]]

                for i, attr_str in enumerate(info_attr):
                    info_attr = font.render(attr_str, True, (255, 255, 0))
                    screen.blit(info_attr, (info_x + 250, info_y + i * 20))

            for i, text_str in enumerate(info_texts):
                info_text = font.render(text_str, True, (255, 255, 0))
                screen.blit(info_text, (info_x, info_y + i * 20))

        for child in self.children:
            child.draw(screen)

class GUILabel:
    color = (255, 255, 255)
    link_color = (0, 102, 204)

    def __init__(self, parent):
        self.parent = parent
        self.text = ""
        self.color = self.__class__.color
        self.margin = (0, 0, 0, 0)
        self.auto_stretch_vertical = True
        self.font = None
        self.link_text = None
        self.link_url = None
        self.link_rect = None
        self.link_color = self.__class__.link_color

    def print_parent(self, parent):
        print(f"[GUILABEL] Parent-Fenster: {parent.title}")

    def _ensure_font(self):
        if self.font is None:
            self.font = pygame.font.SysFont("Verdana", 12)

    def _wrap_text(self):
        if not self.text:
            return []

        self._ensure_font()
        max_width = self.parent.width - self.margin[0] - self.margin[2]

        paragraphs = self.text.splitlines()
        lines = []

        for paragraph in paragraphs:
            words = paragraph.split(" ")
            current_line = ""

            for word in words:
                test_line = current_line + (" " if current_line else "") + word
                if self.font.size(test_line)[0] <= max_width:
                    current_line = test_line
                else:
                    if current_line:
                        lines.append(current_line)
                    current_line = word

            if current_line:
                lines.append(current_line)

            lines.append("")

        if lines and lines[-1] == "":
            lines.pop()

        return lines

    def SetText(self, text):
        self.text = text
        self.link_text = None
        self.link_url = None
        print(f"[GUILABEL] Text gesetzt: {text}")
        
    def SetLink(self, text, url):
        self.link_text = text
        self.link_url = url
        print(f"[GUILABEL] Link gesetzt: {text} -> {url}")

    def SetTextColor(self, r, g, b):
        self.color = r, g, b
        print(f"[GUILABEL] Textfarbe geandert: ({r}, {g}, {b})")

    def Margin(self, left, top, right, bottom):
        self.margin = (left, top, right, bottom)
        print(f"[GUILABEL] Margin gesetzt: ({left}, {top}, {right}, {bottom})")

    def SetAutoStretchVertical(self, state):
        self.auto_stretch_vertical = bool(state)

    def draw(self, screen):
        if not self.parent.visible:
            return
        self._ensure_font()
        x = self.parent.x + self.margin[0]
        y = self.parent.y + GUIWindow.TITLE_BAR_HEIGHT + self.margin[1]

        lines = self._wrap_text()
        line_height = self.font.get_linesize()

        for i, line in enumerate(lines):
            text_surf = self.font.render(line, True, self.color)
            screen.blit(text_surf, (x, y + i * line_height))

        if self.link_text and self.link_url:
            link_surf = self.font.render(self.link_text, True, self.link_color)
            self.link_rect = link_surf.get_rect(topleft=(x, y + len(lines) * line_height + 5))
            screen.blit(link_surf, self.link_rect)
            pygame.draw.line(
                screen, self.link_color,
                (self.link_rect.left, self.link_rect.bottom),
                (self.link_rect.right, self.link_rect.bottom),
                1
            )

    def handle_event(self, event):
        if self.link_text and self.link_url and self.link_rect:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.link_rect.collidepoint(event.pos):
                    webbrowser.open(self.link_url)
                    return True
        return False

class GUIButton:
    bg_color = (80, 80, 80)
    hover_color = (100, 100, 100)
    text_color = (255, 255, 255)

    def __init__(self, parent):
        self.parent = parent
        self.text = "Button"
        self.margin = (0, 0, 0, 0)
        self.width = 100
        self.height = 30
        self.bg_color = self.__class__.bg_color
        self.hover_color = self.__class__.hover_color
        self.text_color = self.__class__.text_color
        self.font = None
        self.hover = False
        self.OnClick = None

    def print_parent(self, parent):
        print(f"[GUIBUTTON] Parent-Fenster: {parent.title}")

    def _ensure_font(self):
        if self.font is None:
            self.font = pygame.font.SysFont("Verdana", 12)

    def SetText(self, text):
        self.text = text
        print(f"[GUIBUTTON] Text gesetzt: {text}")

    def Margin(self, left, top, right, bottom):
        self.margin = (left, top, right, bottom)
        print(f"[GUIBUTTON] Margin gesetzt: ({left}, {top}, {right}, {bottom})")

    def SetSize(self, w, h):
        self.width, self.height = w, h
        print(f"[GUIBUTTON] Grosse geandert: {w}x{h}")

    def draw(self, screen):
        if not self.parent.visible:
            return

        self._ensure_font()

        x = self.parent.x + self.margin[0]
        y = self.parent.y + GUIWindow.TITLE_BAR_HEIGHT + self.margin[1]

        color = self.hover_color if self.hover else self.bg_color
        pygame.draw.rect(screen, color, (x, y, self.width, self.height), border_radius=4)
        text_surf = self.font.render(self.text, True, self.text_color)
        text_rect = text_surf.get_rect(center=(x + self.width / 2, y + -2 + self.height / 2))
        screen.blit(text_surf, text_rect)

    def handle_event(self, event):
        x = self.parent.x + self.margin[0]
        y = self.parent.y + GUIWindow.TITLE_BAR_HEIGHT + self.margin[1]
        rect = pygame.Rect(x, y, self.width, self.height)

        if event.type == pygame.MOUSEMOTION:
            self.hover = rect.collidepoint(event.pos)

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if rect.collidepoint(event.pos): 
                if self.OnClick:
                    try:
                        self.OnClick()
                    except Exception as e:
                        print("[GUIBUTTON]", f"Fehler beim Klick-Callback: {e}")
                return True

        return False

class GUITextEntry:
    bg_color = (50, 50, 50)
    border_color = (80, 80, 80)
    active_border_color = (0, 150, 255)
    text_color = (255, 255, 255)
    placeholder_color = (120, 120, 120)

    def __init__(self, parent):
        self.parent = parent
        self.text = ""
        self.placeholder = "Enter text..."
        self.margin = (0, 0, 0, 0)
        self.width = 200
        self.height = 30
        self.bg_color = self.__class__.bg_color
        self.border_color = self.__class__.border_color
        self.active_border_color = self.__class__.active_border_color
        self.text_color = self.__class__.text_color
        self.place_holder_color = self.__class__.placeholder_color
        self.font = None
        self.active = False
        self.cursor_visible = True
        self.cursor_time = 0
        self.max_length = 100
        self.OnChange = None
        self.OnEnter = None

    def print_parent(self, parent):
        print(f"[GUITEXTENTRY] Parent-Fenster: {parent.title}")

    def _ensure_font(self):
        if self.font is None:
            self.font = pygame.font.SysFont("Verdana", 12)

    def SetText(self, text):
        self.text = text
        print(f"[GUITEXTENTRY] Text gesetzt: {text}")

    def GetText(self):
        return self.text

    def SetPlaceholder(self, text):
        self.placeholder = text
        print(f"[GUITEXTENTRY] Placeholder gesetzt: {text}")

    def Margin(self, left, top, right, bottom):
        self.margin = (left, top, right, bottom)
        print(f"[GUITEXTENTRY] Margin gesetzt: ({left}, {top}, {right}, {bottom})")

    def SetSize(self, w, h):
        self.width, self.height = w, h
        print(f"[GUITEXTENTRY] Grosse geandert: {w}x{h}")

    def SetMaxLength(self, length):
        self.max_length = length
        print(f"[GUITEXTENTRY] Maximale Textlange gesetzt: {length}")

    def draw(self, screen):
        if not self.parent.visible:
            return

        self._ensure_font()

        x = self.parent.x + self.margin[0]
        y = self.parent.y + GUIWindow.TITLE_BAR_HEIGHT + self.margin[1]

        # Background
        pygame.draw.rect(screen, self.bg_color, (x, y, self.width, self.height), border_radius=4)

        # Border (active or inactive)
        border_color = self.active_border_color if self.active else self.border_color
        pygame.draw.rect(screen, border_color, (x, y, self.width, self.height), width=2, border_radius=4)

        # Text or Placeholder
        padding  = 8
        display_text = self.text if self.text else self.placeholder
        text_color = self.text_color if self.text else self.place_holder_color

        text_surf = self.font.render(display_text, True, text_color)

        # Text Clipping
        clip_rect = pygame.Rect(x + padding, y, self.width - padding * 2, self.height)
        screen.set_clip(clip_rect)

        text_y = y + (self.height - text_surf.get_height()) // 2
        screen.blit(text_surf, (x + padding, text_y))

        # Cursor
        if self.active:
            self.cursor_time += 1
            if self.cursor_time > 120:
                self.cursor_visible = not self.cursor_visible
                self.cursor_time = 0

            if self.cursor_visible:
                cursor_x = x + padding + self.font.size(self.text)[0]
                cursor_y = y + 6
                pygame.draw.line(screen, self.text_color,
                                 (cursor_x, cursor_y),
                                 (cursor_x, cursor_y + self.height - 12), 2)

        screen.set_clip(None)

    def handle_event(self, event):
        x = self.parent.x + self.margin[0]
        y = self.parent.y + GUIWindow.TITLE_BAR_HEIGHT + self.margin[1]
        rect = pygame.Rect(x, y, self.width, self.height)

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.active = rect.collidepoint(event.pos)
            if self.active:
                self.cursor_visible = True
                self.cursor_time = 0
            return self.active

        if self.active and event.type == pygame.KEYDOWN:
            old_text = self.text

            if event.key == pygame.K_RETURN:
                if self.OnEnter:
                    try:
                        self.OnEnter(self.text)
                    except Exception as e:
                        print("[GUITEXTENTRY]", f"Fehler beim Enter-Callback: {e}")
                return True

            elif event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]

            elif len(self.text) < self.max_length:
                if event.unicode and event.unicode.isprintable():
                    self.text += event.unicode

            if old_text != self.text and self.OnChange:
                try:
                    self.OnChange(self.text)
                except Exception as e:
                    print("[GUITEXTENTRY]", f"Fehler beim Change-Callback: {e}")

            self.cursor_visible = True
            self.cursor_time = 0
            return True

        return False

class VHSMenu:
    def __init__(self):
        self.active = False
        self.items = [
            ("FENSTERLISTE", self.show_windows, "Zeige alle aktiven Fenster"),
            ("FPS ANZEIGEN", self.toggle_fps, "Toggle FPS Counter"),
            ("LUA NEU LADEN", self.reload_lua, "Lade script.lua neu"),
            ("GUI RESETTEN", self.reset_gui, "Loesche alle Fenster"),
            ("SCHLIESSEN", self.toggle_menu, "Schliesse dieses Menu")
        ]
        self.selected = 0
        self.font = pygame.font.SysFont("Courier New", 14, bold=True)
        self.font_small = pygame.font.SysFont("Courier New", 11)
        self.font_title = pygame.font.SysFont("Courier New", 20, bold=True)
        self.show_fps = False
        self.last_fps = 0
        self.scanline_offset = 0
        self.glitch_timer = 0
        self.menu_animation = 0
        
    def toggle_menu(self):
        self.active = not self.active
        self.menu_animation = 0
        print("[VHS]", f"VHS Menu {'aktiviert' if self.active else 'geschlossen'}")
        debug.log(f"VHS Menu {'aktiviert' if self.active else 'geschlossen'}")
        
    def handle_event(self, event):
        if not self.active:
            return False
            
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected = (self.selected - 1) % len(self.items)
                return True
            elif event.key == pygame.K_DOWN:
                self.selected = (self.selected + 1) % len(self.items)
                return True
            elif event.key == pygame.K_RETURN:
                _, func, _ = self.items[self.selected]
                func()
                return True
            elif event.key == pygame.K_ESCAPE:
                self.toggle_menu()
                return True
                
        return True
    
    def draw(self, screen):
        if not self.active:
            if self.show_fps:
                self._draw_fps_overlay(screen)
            return
        
        # Animation
        if self.menu_animation < 1.0:
            self.menu_animation = min(1.0, self.menu_animation + 0.1)
        
        width, height = 420, 340
        x = screen.get_width() // 2 - width // 2
        y = screen.get_height() // 2 - height // 2
        
        # Animierter Einzug
        anim_y = y - int((1 - self.menu_animation) * 50)
        
        # Haupthintergrund mit VHS-Effekt
        bg = pygame.Surface((width, height), pygame.SRCALPHA)
        bg.fill((10, 12, 15, 230))
        
        # Äußerer Rahmen (VHS-Style)
        pygame.draw.rect(bg, (0, 255, 100), (0, 0, width, height), 3)
        pygame.draw.rect(bg, (0, 180, 70), (3, 3, width-6, height-6), 1)
        
        # Header
        header_height = 45
        pygame.draw.rect(screen, (0, 220, 80), (x, anim_y, width, header_height))
        pygame.draw.rect(screen, (0, 255, 100), (x, anim_y, width, header_height), 2)
        
        # Titel
        title = self.font_title.render("< VHS DEBUG SYSTEM >", True, (0, 0, 0))
        title_x = x + width // 2 - title.get_width() // 2
        screen.blit(title, (title_x, anim_y + 12))
        
        # Zeitstempel
        import datetime
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        time_surf = self.font_small.render(timestamp, True, (0, 0, 0))
        screen.blit(time_surf, (x + width - time_surf.get_width() - 10, anim_y + 15))
        
        # Menü-Items
        item_start_y = anim_y + header_height + 20
        for i, (label, _, desc) in enumerate(self.items):
            item_y = item_start_y + i * 50
            
            # Auswahlhintergrund
            if i == self.selected:
                select_surf = pygame.Surface((width - 20, 44), pygame.SRCALPHA)
                select_surf.fill((0, 255, 100, 60))
                screen.blit(select_surf, (x + 10, item_y - 2))
                pygame.draw.rect(screen, (0, 255, 100), (x + 10, item_y - 2, width - 20, 44), 2)
                
                # Animierter Pfeil
                arrow_offset = int(math.sin(pygame.time.get_ticks() / 200) * 3)
                arrow = self.font.render(">", True, (0, 255, 255))
                screen.blit(arrow, (x + 15 + arrow_offset, item_y + 2))
                label_x = x + 40
                color = (0, 255, 255)
            else:
                label_x = x + 25
                color = (150, 255, 150)
            
            # Label
            label_surf = self.font.render(label, True, color)
            screen.blit(label_surf, (label_x, item_y + 2))
            
            # Beschreibung
            desc_surf = self.font_small.render(desc, True, (100, 180, 100))
            screen.blit(desc_surf, (label_x, item_y + 22))
        
        # FPS falls aktiviert
        if self.show_fps:
            self._draw_fps_overlay(screen)
    
    def _draw_fps_overlay(self, screen):
        """Zeichnet FPS-Anzeige im VHS-Style"""
        fps_width, fps_height = 140, 74
        fps_x, fps_y = 15, 15
        
        # Hintergrund
        fps_bg = pygame.Surface((fps_width, fps_height), pygame.SRCALPHA)
        fps_bg.fill((10, 12, 15, 200))
        pygame.draw.rect(fps_bg, (0, 255, 100), (0, 0, fps_width, fps_height), 2)
        screen.blit(fps_bg, (fps_x, fps_y))
        
        # FPS Label
        label = self.font_small.render("FRAME RATE", True, (100, 200, 100))
        screen.blit(label, (fps_x + 8, fps_y + 5))
        
        # FPS Wert
        fps_val = int(self.last_fps)
        if fps_val >= 150:
            color = (0, 255, 100)
        elif fps_val >= 30:
            color = (255, 255, 0)
        else:
            color = (255, 50, 50)
        
        fps_text = self.font_title.render(f"{fps_val}", True, color)
        screen.blit(fps_text, (fps_x + 10, fps_y + 20))
        
        # "FPS" klein
        fps_label = self.font_small.render("FPS", True, color)
        screen.blit(fps_label, (fps_x + fps_text.get_width() + 15, fps_y + 28))
        
        # Live-Diagramm
        graph_width = fps_width - 20
        graph_height = 18
        graph_x = fps_x + 10
        graph_y = fps_y + 47
    
        # Hintergrund des Diagramms
        pygame.draw.rect(screen, (20, 25, 30), (graph_x, graph_y, graph_width, graph_height))
        pygame.draw.rect(screen, (50, 50, 50), (graph_x, graph_y, graph_width, graph_height), 1)
    
        # FPS-Historie aktualisieren (falls nicht vorhanden, initialisieren)
        if not hasattr(self, 'fps_history'):
            self.fps_history = []
    
        self.fps_history.append(fps_val)
        max_points = graph_width // 2  # Ein Punkt alle 2 Pixel
        if len(self.fps_history) > max_points:
            self.fps_history.pop(0)
    
        # Diagramm zeichnen
        if len(self.fps_history) > 1:
            max_fps = 400  # Referenzwert für Skalierung
            points = []
            for i, fps in enumerate(self.fps_history):
                x = graph_x + (i * graph_width // max_points)
                normalized_fps = min(fps, max_fps) / max_fps
                y = graph_y + graph_height - int(normalized_fps * graph_height)
                points.append((x, y))
        
            # Linie zeichnen
            if len(points) > 1:
                pygame.draw.lines(screen, color, False, points, 2)
            
    def show_windows(self):
        print("[SIMPLEGUI]", "=" * 40)
        debug.log("=" * 40)
        print("[SIMPLEGUI] AKTIVE FENSTER:")
        debug.log("AKTIVE FENSTER:")
        for win in SimpleGUI.windows:
            print("[SIMPLEGUI]", f" > {win.title} @ ({win.x}, {win.y})")
            debug.log(f" > {win.title} @ ({win.x}, {win.y})")
        print("[SIMPLEGUI]", "=" * 40)
        debug.log("=" * 40)
        
    def toggle_fps(self):
        self.show_fps = not self.show_fps
        print(f"[VHS] FPS Anzeige {'aktiviert' if self.show_fps else 'deaktiviert'}")
        debug.log(f"[VHS] FPS Anzeige {'aktiviert' if self.show_fps else 'deaktiviert'}")
        
    def reload_lua(self):
        try: 
            with open("script.lua", "r", encoding="utf-8") as f:
                lua_code = f.read()
            lua.execute(lua_code)
            print("[VHS] Lua Skript erfolgreich neu geladen")
            debug.log("[VHS]  Skript erfolgreich neu geladen")
        except Exception as e:
            print(f"[VHS] FEHLER beim Neuladen: {e}")
            debug.log(f"[VHS] FEHLER beim Neuladen: {e}")
            
    def reset_gui(self):
        SimpleGUI.windows.clear()
        print("[VHS] GUI zureuckgesetzt - alle Fenster entfernt")
        debug.log("[VHS] GUI zureuckgesetzt - alle Fenster entfernt")

class DebugOverlay:
    def __init__(self, max_messages=16):
        self.messages = []
        self.max_messages = max_messages
        self.font = pygame.font.SysFont("Consolas", 12)
        self.bg_color = (30, 30, 30, 160)
        self.text_color = (200, 200, 200)
        self.active = False

    def log(self, msg):
        self.messages.append(msg)
        if len(self.messages) > self.max_messages:
            self.messages.pop(0)

    def toggle_log(self):
        self.active = not self.active


    def draw(self, screen):
        if not self.messages or not self.active:
            return

        padding = 10
        line_height = self.font.get_linesize()
        width = 400
        height = line_height * len(self.messages) + padding * 2
        x = screen.get_width() - width - 15
        y = 15

        surface = pygame.Surface((width, height), pygame.SRCALPHA)
        surface.fill(self.bg_color)
        pygame.draw.rect(surface, (80, 80, 80), (0, 0, width, height), 2)

        for i, msg in enumerate(self.messages):
            text = self.font.render(msg, True, self.text_color)
            surface.blit(text, (padding, padding + i * line_height))

        screen.blit(surface, (x, y))