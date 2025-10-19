# SimpleGUI-Lua-Engine
SimpleGUI is a Lua engine that allows you to create windows in your own environment. The Lua syntax is very lightweight and customizable. \
**THIS PROJECT IS CURRENTLY MOST IN GERMAN, I WILL TRANSLATE IT IN ENGLISH!**

# Utilitys
The window resolution is currently permanently set to 1920 x 1080, but you can change this in SimpleGUI.py:
````python
screen = pygame.display.set_mode((1920, 1080), pygame.FULLSCREEN)
````
 If you want to use Center(), you also need to adjust the resolution in the GUIWindow class's Center() method:
````python
    def Center(self):
        self.x = (1920 - self.width) / 2
        self.y = (1080 - self.height) / 2
        print("[GUIWINDOW] Fenster zentriert") 
````

# Lua Scripting
The engine is based on VGUI from Garry's Mod. The syntax is very similar, and that's what ultimately gave me the idea to build something like this.

The most important thing is what is written at the beginning of the file: 
````lua
local windows = {}
````
This is the list of windows for your environment and is also used in Python.

## SimpleGUI Windows
Creating windows is not difficult, the hardest thing is being able to arrange all the elements in them nicely.

Here is an example of how you could create a window:
````lua
local frame = SimpleGUI.Create("Window")
````

Here is how you set the title:
````lua
frame:SetTitle("This is my Window")
````

Here is how you set the Size:
````lua
frame:SetSize(480, 260)
````

You can use either:
````lua
frame:Center()
````
or:
````lua
frame:SetPos(300, 500)
````
to place the window either in the center or at a custom position.

Now come the things that every window should have, but here you can turn them off.
````lua
frame:SetDraggable(true)
frame:ShowCloseButton(true)
````

When you are done with all properties AND objects it is recommended to write this:
````lua
table.insert(windows, frame)
````

## SimpleGUI Label
A label is used to display simple text. You can also use ````\n```` to create a newline.

You can now create a local variable with the name you want for the label. Here's how:
````lua
local label = SimpleGUI.Create("Label", frame)
````
The ````frame```` (or whatever the name of the window it should be in) in ````SimpleGUI.Create("Label", frame)```` is important because it tells the function what the parent window is. If the parent window isn't specified or doesn't exist, a ValueError occurs.

You can now specify the text in the label:
````lua
label:SetText("Some Text in here\nwith a newline.")
````
Or you can create a link with:
````lua
label:SetLink("Click Me!", "https://example.com")
````
You can't use both in one label because it will overwrite itself! 

You can also specify the color for the label. It's important to enter an RGB value, not a hex value. For example:
````lua
label:SetTextColor(50, 70, 90)
````

And now comes a function that's used in virtually every object you can create. Here, with a label:
````lua
label:Margin(10, 10, 10, 10)
````

The Margin function is structured and used in the following pattern: ````Margin(left, top, right, bottom)````
As I mentioned, this function is used in every object and is the basic function for positioning objects.

## SimpleGUI Buttons
Next, we come to the buttons. You create them by creating a local variable:
````lua
local button = SimpleGUI.Create("Button", frame)
````

You can edit the text in the button with this:
````lua
button:SetText("Press me!")
````

To determine the size of the buttons use this:
````lua
button:SetSize(200, 400p)
````
The size is like in HTML, width x height in pixels.

And the margin is set like the others:
````lua
button:Margin(10, 10, 10, 10)
````

The buttons have a special function that can also be used:
````lua
button.OnClick = function()
    print("Button was clicked")
end
````
Everything in this function will be executed when the button is pressed.

# SimpleGUI Textentrys
These are simple text inputs that can be easily controlled.

How to create a text entry:
````lua
local entry = SimpleGUI.Create("TextEntry", frame)
````

Here you can program a placeholder that disappears as soon as you click on it. Here's an example: 
````lua
entry:SetPlaceholder("Type some Thing here")
````

To adjust the size you need this:
````lua
entry:SetSize(200, 50)
````

To set the maximum number of characters in a text input, you must use this, the default is 50:
````lua
entry:SetMaxLength(40)
````

If you want to read the text in the text entry use this:
````lua
local text = entry:GetText()
print("Your text is:" .. text)
````

---
# Debug Functions
- F2: Main Debug menu
     - Print All active Windows
     - Show FPS
     - Reset GUI
     - Reload Lua Script
     - Close
- F3: Show Debug Log
     - All debug print that were printed via ````debug.log````
- F4: Show Debug Values
     - like F3 in Minecraft
     - F4 + shift for all attributes
- F5: Execute the Lua callback script

## Graphics
The tick speed is currently very high (1000) and only intended for good GPUs and CPUs. If you have a slightly less powerful PC, you should lower this a bit. Here is were:
````python
    clock.tick(1000)
```` 
(in SimpleGUI.py) 
