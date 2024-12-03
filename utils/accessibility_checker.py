from bs4 import BeautifulSoup

class AccessibilityChecker:
    def __init__(self, html_content):
        self.soup = BeautifulSoup(html_content, 'html.parser')
        
    def analyze(self):
        issues = []
        
        # Check for image alt texts
        self._check_images(issues)
        # Check for heading hierarchy
        self._check_headings(issues)
        # Check for form labels
        self._check_forms(issues)
        # Check for ARIA roles
        self._check_aria(issues)
        
        return issues
    
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
