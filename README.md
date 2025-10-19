# SimpleGUI-Lua-Engine
SimpleGUI is a Lua engine that allows you to create windows in your own environment. The Lua syntax is very lightweight and customizable.

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

Now come the things that every window should have, but here you can turn them off.
````lua
frame:SetDraggable(true)
frame:ShowCloseButton(true)
````

When you are done with all properties AND objects it is recommended to write this:
````lua
table.insert(windows, frame)
````
