local windows = {}
local rainbow_active = false
local rainbow_frame = nil

-- Zufallsfunktionen
local function rand_color()
    return math.random(50,255), math.random(50,255), math.random(50,255)
end

local function rand_pos(max_x, max_y)
    return math.random(50, max_x or 800), math.random(50, max_y or 500)
end

-- Regenbogenmodus aktivieren/deaktivieren
local function toggle_rainbow_mode()
    if rainbow_active then
        rainbow_active = false
        print("Regenbogenmodus deaktiviert")
        return
    end

    rainbow_active = true
    print("Regenbogenmodus aktiviert")

    coroutine.wrap(function()
        while rainbow_active and rainbow_frame do
            local r, g, b = rand_color()
            rainbow_frame:SetBackgroundColor(r, g, b)
            coroutine.yield()
        end
    end)()
end

-- Erstellt ein zufaelliges Fenster
local function spawn_window()
    local frame = SimpleGUI.Create("Window")
    frame:SetTitle("Zufallsfenster #" .. tostring(#windows + 1))
    frame:SetSize(math.random(150, 300), math.random(120, 220))
    local x, y = rand_pos()
    frame:SetPos(x, y)
    frame:ShowCloseButton(true)
    frame:SetDraggable(true)

    local label = SimpleGUI.Create("Label", frame)
    label:SetText("Ich bin ein zufaelliges Fenster.\nDruecke den Button unten.")
    label:SetTextColor(rand_color())
    label:Margin(10, 10, 10, 10)

    local move_btn = SimpleGUI.Create("Button", frame)
    move_btn:SetText("Bewege mich")
    move_btn:SetSize(120, 25)
    move_btn:Margin(20, 60, 10, 10)
    move_btn.OnClick = function()
        local nx, ny = rand_pos()
        frame:SetPos(nx, ny)
        print("Fenster verschoben nach:", nx, ny)
    end

    table.insert(windows, frame)
end

-- Hauptfenster
local function create_manager_window()
    local frame = SimpleGUI.Create("Window")
    frame:SetTitle("SimpleGUI Fun Manager")
    frame:SetSize(480, 260)
    frame:Center()
    frame:SetDraggable(true)
    frame:ShowCloseButton(true)

    local label = SimpleGUI.Create("Label", frame)
    label:SetText("Willkommen beim SimpleGUI Fun Manager.\nErzeuge Fenster, bewege sie oder starte den Regenbogenmodus.")
    label:SetAutoStretchVertical(true)
    label:Margin(20, 20, 10, 10)

    local spawn_btn = SimpleGUI.Create("Button", frame)
    spawn_btn:SetText("Fenster spawnen")
    spawn_btn:SetSize(150, 30)
    spawn_btn:Margin(30, 120, 10, 10)
    spawn_btn.OnClick = function()
        spawn_window()
    end

    local rainbow_btn = SimpleGUI.Create("Button", frame)
    rainbow_btn:SetText("Regenbogen Fenster")
    rainbow_btn:SetSize(180, 30)
    rainbow_btn:Margin(200, 120, 10, 10)
    rainbow_btn.OnClick = function()
        if not rainbow_frame then
            rainbow_frame = SimpleGUI.Create("Window")
            rainbow_frame:SetTitle("Regenbogenfenster")
            rainbow_frame:SetSize(300, 150)
            rainbow_frame:SetDraggable(true)
            rainbow_frame:ShowCloseButton(true)
            local lbl = SimpleGUI.Create("Label", rainbow_frame)
            lbl:SetText("Ich wechsle meine Farbe.\nKlicke den Button erneut zum Stoppen.")
            lbl:Margin(10, 10, 10, 10)
        end
        toggle_rainbow_mode()
    end

    local close_all_btn = SimpleGUI.Create("Button", frame)
    close_all_btn:SetText("Alle Fenster schliessen")
    close_all_btn:SetSize(200, 30)
    close_all_btn:Margin(130, 180, 10, 10)
    close_all_btn.OnClick = function()
        for _, w in ipairs(windows) do
            w:Close()
        end
        windows = {}
        if rainbow_frame then
            rainbow_frame:Close()
            rainbow_frame = nil
        end
        print("Alle Fenster geschlossen.")
    end

    table.insert(windows, frame)
end

create_manager_window()

local function try_new_textentry()
    local frame = SimpleGUI.Create("Window")
    frame:SetTitle("Try New Textentry Function")
    frame:SetSize(480, 260)
    frame:SetDraggable(true)
    frame:ShowCloseButton(true)

    local entry = SimpleGUI.Create("TextEntry", frame)
    entry:SetSize(200, 25)
    entry:Margin(20, 20, 10, 10)
    entry:SetPlaceholder("Type something here...")
end

try_new_textentry()