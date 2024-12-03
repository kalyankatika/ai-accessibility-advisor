from bs4 import BeautifulSoup
from .custom_rules import CustomRuleManager, CustomRule

class AccessibilityChecker:
    def __init__(self, html_content):
        self.soup = BeautifulSoup(html_content, 'html.parser')
        self.custom_rule_manager = CustomRuleManager()
        
    def analyze(self):
        issues = []
        
        # Existing checks
        self._check_images(issues)
        self._check_headings(issues)
        self._check_forms(issues)
        self._check_aria(issues)
        
        # New WCAG 2.1 checks
        self._check_keyboard_navigation(issues)
        self._check_focus_management(issues)
        self._check_skip_links(issues)
        self._check_language(issues)
        self._check_document_structure(issues)
        self._check_tables(issues)
        self._check_lists(issues)
        self._check_multimedia(issues)
        
        # Evaluate custom rules
        custom_issues = self.custom_rule_manager.evaluate_rules(self.soup)
        issues.extend(custom_issues)
        
        return issues

    def add_custom_rule(self, rule: CustomRule):
        """Add a custom accessibility rule."""
        self.custom_rule_manager.add_rule(rule)
        
    def remove_custom_rule(self, rule_name: str):
        """Remove a custom accessibility rule."""
        self.custom_rule_manager.remove_rule(rule_name)
        
    def get_custom_rule(self, rule_name: str) -> CustomRule:
        """Get a custom accessibility rule by name."""
        return self.custom_rule_manager.get_rule(rule_name)
    
    def _check_images(self, issues):
        images = self.soup.find_all('img')
        for img in images:
            if not img.get('alt'):
                issues.append({
                    'type': 'error',
                    'category': 'Images',
                    'message': f'Image missing alt text: {img}',
                    'recommendation': 'Add descriptive alt text to the image'
                })

    def _check_headings(self, issues):
        headings = self.soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
        prev_level = 0
        for heading in headings:
            current_level = int(heading.name[1])
            if current_level - prev_level > 1:
                issues.append({
                    'type': 'warning',
                    'category': 'Headings',
                    'message': f'Heading level skipped from h{prev_level} to h{current_level}',
                    'recommendation': 'Maintain proper heading hierarchy'
                })
            prev_level = current_level

    def _check_forms(self, issues):
        inputs = self.soup.find_all('input')
        for input_elem in inputs:
            if input_elem.get('type') not in ['submit', 'button', 'hidden']:
                label = self.soup.find('label', {'for': input_elem.get('id')})
                if not label:
                    issues.append({
                        'type': 'error',
                        'category': 'Forms',
                        'message': f'Input missing label: {input_elem}',
                        'recommendation': 'Add proper label for the input field'
                    })

    def _check_aria(self, issues):
        elements_with_aria = self.soup.find_all(lambda tag: any(attr.startswith('aria-') for attr in tag.attrs))
        for element in elements_with_aria:
            if 'role' not in element.attrs:
                issues.append({
                    'type': 'warning',
                    'category': 'ARIA',
                    'message': f'Element with ARIA attributes missing role: {element}',
                    'recommendation': 'Add appropriate role attribute'
                })

    def _check_keyboard_navigation(self, issues):
        # Check for positive tabindex values
        elements_with_tabindex = self.soup.find_all(lambda tag: 'tabindex' in tag.attrs)
        for element in elements_with_tabindex:
            tabindex = element.get('tabindex')
            try:
                if int(tabindex) > 0:
                    issues.append({
                        'type': 'warning',
                        'category': 'Keyboard Navigation',
                        'message': f'Positive tabindex value found: {element}',
                        'recommendation': 'Avoid using positive tabindex values as they disrupt natural tab order'
                    })
            except ValueError:
                pass

        # Check for potential keyboard traps
        interactive_elements = self.soup.find_all(['button', 'a', 'input', 'select', 'textarea'])
        for element in interactive_elements:
            if element.get('onclick') and not element.get('onkeypress'):
                issues.append({
                    'type': 'error',
                    'category': 'Keyboard Navigation',
                    'message': f'Element with onclick but no keyboard event handler: {element}',
                    'recommendation': 'Ensure all interactive elements are keyboard accessible'
                })

    def _check_focus_management(self, issues):
        elements_with_focus = self.soup.find_all(['button', 'a', 'input', 'select', 'textarea'])
        for element in elements_with_focus:
            if element.get('style') and ('outline: none' in element.get('style') or 'outline:none' in element.get('style')):
                issues.append({
                    'type': 'error',
                    'category': 'Focus Management',
                    'message': 'Focus outline removed from interactive element',
                    'recommendation': 'Maintain visible focus indicators for keyboard navigation'
                })

    def _check_skip_links(self, issues):
        skip_links = self.soup.find_all('a', href='#main-content') or self.soup.find_all('a', text=lambda t: t and 'skip' in t.lower())
        if not skip_links:
            issues.append({
                'type': 'warning',
                'category': 'Navigation',
                'message': 'No skip links found at the beginning of the page',
                'recommendation': 'Add skip links to bypass repetitive navigation'
            })

    def _check_language(self, issues):
        html_tag = self.soup.find('html')
        if not html_tag or not html_tag.get('lang'):
            issues.append({
                'type': 'error',
                'category': 'Language',
                'message': 'HTML lang attribute missing',
                'recommendation': 'Add a valid lang attribute to the HTML element'
            })

    def _check_document_structure(self, issues):
        # Check for main landmark
        if not self.soup.find('main') and not self.soup.find(role='main'):
            issues.append({
                'type': 'error',
                'category': 'Document Structure',
                'message': 'No main landmark found',
                'recommendation': 'Add a <main> element or role="main" to identify the main content'
            })

        # Check for other important landmarks
        landmarks = {
            'header': 'banner',
            'nav': 'navigation',
            'footer': 'contentinfo'
        }
        for tag, role in landmarks.items():
            if not self.soup.find(tag) and not self.soup.find(role=role):
                issues.append({
                    'type': 'warning',
                    'category': 'Document Structure',
                    'message': f'No {tag} landmark found',
                    'recommendation': f'Add a <{tag}> element or role="{role}" for better document structure'
                })

    def _check_tables(self, issues):
        tables = self.soup.find_all('table')
        for table in tables:
            if not table.find('caption'):
                issues.append({
                    'type': 'warning',
                    'category': 'Tables',
                    'message': 'Table missing caption',
                    'recommendation': 'Add a caption to describe the table content'
                })
            
            if not table.find_all('th'):
                issues.append({
                    'type': 'error',
                    'category': 'Tables',
                    'message': 'Table missing header cells',
                    'recommendation': 'Use <th> elements to identify table headers'
                })

    def _check_lists(self, issues):
        lists = self.soup.find_all(['ul', 'ol'])
        for list_elem in lists:
            if not list_elem.find_all('li'):
                issues.append({
                    'type': 'error',
                    'category': 'Lists',
                    'message': 'Empty list found',
                    'recommendation': 'Remove empty lists or add list items'
                })
            
            for child in list_elem.children:
                if child.name and child.name != 'li':
                    issues.append({
                        'type': 'error',
                        'category': 'Lists',
                        'message': 'List contains non-list item elements',
                        'recommendation': 'Use only <li> elements as direct children of lists'
                    })

    def _check_multimedia(self, issues):
        # Check video elements
        videos = self.soup.find_all('video')
        for video in videos:
            if not video.find('track', type='captions'):
                issues.append({
                    'type': 'error',
                    'category': 'Multimedia',
                    'message': 'Video missing captions',
                    'recommendation': 'Add captions using the <track> element'
                })

        # Check audio elements
        audios = self.soup.find_all('audio')
        for audio in audios:
            if not self.soup.find('a', href=lambda x: x and x.endswith(('.txt', '.pdf'))):
                issues.append({
                    'type': 'warning',
                    'category': 'Multimedia',
                    'message': 'Audio content might be missing transcript',
                    'recommendation': 'Provide a transcript for audio content'
                })
