from bs4 import BeautifulSoup
import re

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
        
        return issues
    
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
