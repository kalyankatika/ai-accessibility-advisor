from bs4 import BeautifulSoup
import re
import colorsys

class ColorValidator:
    def __init__(self, html_content):
        self.soup = BeautifulSoup(html_content, 'html.parser')
        self.fds_colors = {
            'green': ['#36B727', '#044014', '#4AD539'],
            'neutral': '#F9F7F5'
        }
        
    def validate(self):
        issues = []
        
        # Check inline styles
        self._check_inline_styles(issues)
        # Check background colors
        self._check_backgrounds(issues)
        # Check button styles
        self._check_buttons(issues)
        # Check color contrast
        self._check_color_contrast(issues)
        
        return issues

    def _hex_to_rgb(self, hex_color):
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

    def _get_relative_luminance(self, rgb):
        r, g, b = [x/255 if x <= 255 else 1.0 for x in rgb]
        r = r/12.92 if r <= 0.03928 else ((r+0.055)/1.055) ** 2.4
        g = g/12.92 if g <= 0.03928 else ((g+0.055)/1.055) ** 2.4
        b = b/12.92 if b <= 0.03928 else ((b+0.055)/1.055) ** 2.4
        return 0.2126 * r + 0.7152 * g + 0.0722 * b

    def _calculate_contrast_ratio(self, color1, color2):
        l1 = self._get_relative_luminance(self._hex_to_rgb(color1))
        l2 = self._get_relative_luminance(self._hex_to_rgb(color2))
        lighter = max(l1, l2)
        darker = min(l1, l2)
        return (lighter + 0.05) / (darker + 0.05)
    
    def _check_inline_styles(self, issues):
        elements = self.soup.find_all(style=True)
        for element in elements:
            style = element['style']
            if 'color' in style or 'background' in style:
                colors = re.findall(r'#[0-9a-fA-F]{6}', style)
                for color in colors:
                    if color not in self.fds_colors['green'] and color != self.fds_colors['neutral']:
                        issues.append({
                            'type': 'error',
                            'category': 'Colors',
                            'message': f'Non-compliant color used: {color}',
                            'recommendation': 'Use FDS approved colors'
                        })

    def _check_color_contrast(self, issues):
        elements = self.soup.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'span', 'a'])
        for element in elements:
            # Get text and background colors
            text_color = self._get_element_color(element, 'color') or '#000000'
            bg_color = self._get_element_background(element) or '#FFFFFF'
            
            contrast_ratio = self._calculate_contrast_ratio(text_color, bg_color)
            
            # WCAG 2.1 Level AA requirements
            is_large_text = self._is_large_text(element)
            required_ratio = 3.0 if is_large_text else 4.5
            
            if contrast_ratio < required_ratio:
                issues.append({
                    'type': 'error',
                    'category': 'Color Contrast',
                    'message': f'Insufficient contrast ratio ({contrast_ratio:.2f}:1) for text element',
                    'recommendation': f'Increase contrast ratio to at least {required_ratio}:1 for {is_large_text and "large" or "normal"} text'
                })

    def _get_element_color(self, element, property_name):
        style = element.get('style', '')
        color_match = re.search(rf'{property_name}:\s*#([0-9a-fA-F]{{6}})', style)
        if color_match:
            return f'#{color_match.group(1)}'
        return None

    def _get_element_background(self, element):
        current = element
        while current:
            bg_color = self._get_element_color(current, 'background-color')
            if bg_color:
                return bg_color
            current = current.parent
        return None

    def _is_large_text(self, element):
        style = element.get('style', '')
        font_size_match = re.search(r'font-size:\s*(\d+)px', style)
        if font_size_match:
            size = int(font_size_match.group(1))
            return size >= 18 or (size >= 14 and 'bold' in style)
        return False
    
    def _check_backgrounds(self, issues):
        elements = self.soup.find_all(class_=True)
        bg_classes = [cls for elem in elements for cls in elem['class'] 
                     if 'bg-' in cls or 'background' in cls]
        
        if not any('bg-neutral' in cls for cls in bg_classes):
            issues.append({
                'type': 'warning',
                'category': 'Background',
                'message': 'Page might not meet 50% neutral background requirement',
                'recommendation': 'Ensure sufficient use of neutral background'
            })

    def _check_buttons(self, issues):
        buttons = self.soup.find_all(['button', 'a'], class_=True)
        for button in buttons:
            if not any('btn-' in cls for cls in button['class']):
                issues.append({
                    'type': 'warning',
                    'category': 'Buttons',
                    'message': 'Button missing FDS styling',
                    'recommendation': 'Apply FDS button classes'
                })
