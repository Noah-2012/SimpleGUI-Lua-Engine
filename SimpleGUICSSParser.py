import re
from typing import Dict, List


class CSSSelector:
    
    def __init__(self, selector: str):
        self._selector = selector
        self._properties = {}
    
    def __setattr__(self, name: str, value):
        if name.startswith('_'):
            super().__setattr__(name, value)
        else:
            self._properties[name] = value
    
    def __getattr__(self, name: str):
        if name.startswith('_'):
            return super().__getattribute__(name)
        return self._properties.get(name)
    
    def __repr__(self):
        props = ', '.join(f'{k}={v}' for k, v in self._properties.items())
        return f"CSSSelector('{self._selector}', {props})"
    
    def __str__(self):
        return self._selector
    
    @property
    def selector(self):
        return self._selector
    
    @property
    def properties(self):
        return self._properties.copy()


class CSSParser:
    
    def __init__(self):
        self.selectors: Dict[str, CSSSelector] = {}
    
    def parse(self, css_string: str) -> Dict[str, CSSSelector]:
        # Entferne Kommentare
        css_string = re.sub(r'/\*.*?\*/', '', css_string, flags=re.DOTALL)
        
        # Regex für CSS-Regeln: Selektor { Eigenschaften }
        pattern = r'([^{]+)\s*\{([^}]+)\}'
        matches = re.finditer(pattern, css_string)
        
        for match in matches:
            selector_name = match.group(1).strip()
            properties_block = match.group(2).strip()
            
            # Erstelle CSSSelector-Objekt
            css_selector = CSSSelector(selector_name)
            
            # Parse Eigenschaften
            properties = self._parse_properties(properties_block)
            
            # Setze Eigenschaften als Attribute
            for prop_name, prop_value in properties.items():
                setattr(css_selector, prop_name, prop_value)
            
            # Speichere Selektor
            self.selectors[selector_name] = css_selector
        
        return self.selectors
    
    def _parse_properties(self, properties_block: str) -> Dict[str, str]:
        properties = {}
        
        # Teile nach Semikolon
        declarations = properties_block.split(';')
        
        for declaration in declarations:
            declaration = declaration.strip()
            if ':' in declaration:
                prop_name, prop_value = declaration.split(':', 1)
                prop_name = prop_name.strip()
                prop_value = prop_value.strip()
                
                # Konvertiere CSS-Eigenschaftsnamen zu Python-Attributnamen
                # z.B. background-color -> background_color
                prop_name = prop_name.replace('-', '_')
                
                properties[prop_name] = prop_value
        
        return properties
    
    def parse_file(self, filename: str) -> Dict[str, CSSSelector]:
        with open(filename, 'r', encoding='utf-8') as f:
            css_string = f.read()
        return self.parse(css_string)
    
    def get(self, selector: str) -> CSSSelector:
        return self.selectors.get(selector)

def hex_to_rgb(hex_color: str) -> tuple[int, int, int]:
    # Entferne optionales '#' am Anfang
    hex_color = hex_color.lstrip('#')
    
    # Überprüfe, ob der Hexwert gültig ist
    if len(hex_color) != 6:
        raise ValueError("Hex-Farbwert muss 6 Zeichen lang sein.")
    
    # Wandle die einzelnen Komponenten um
    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)
    
    return (r, g, b)

def px_to_int(px: str) -> int:
    return int(px.strip().lower().replace("px", ""))
