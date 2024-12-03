from dataclasses import dataclass
from typing import Optional, List, Callable
from bs4 import BeautifulSoup
import re

@dataclass
class CustomRule:
    name: str
    description: str
    selector: str
    condition: str
    message: str
    recommendation: str
    severity: str = "warning"  # "error" or "warning"
    
class CustomRuleManager:
    def __init__(self):
        self.rules: List[CustomRule] = []
        
    def add_rule(self, rule: CustomRule) -> None:
        """Add a new custom accessibility rule."""
        self.rules.append(rule)
        
    def remove_rule(self, rule_name: str) -> None:
        """Remove a custom rule by name."""
        self.rules = [rule for rule in self.rules if rule.name != rule_name]
        
    def get_rule(self, rule_name: str) -> Optional[CustomRule]:
        """Get a custom rule by name."""
        return next((rule for rule in self.rules if rule.name == rule_name), None)
        
    def evaluate_rules(self, soup: BeautifulSoup) -> List[dict]:
        """Evaluate all custom rules against the provided HTML content."""
        issues = []
        
        for rule in self.rules:
            try:
                # Find elements matching the selector
                elements = soup.select(rule.selector)
                
                for element in elements:
                    # Evaluate the condition
                    if self._evaluate_condition(element, rule.condition):
                        issues.append({
                            'type': rule.severity,
                            'category': 'Custom Rule: ' + rule.name,
                            'message': rule.message,
                            'recommendation': rule.recommendation
                        })
            except Exception as e:
                issues.append({
                    'type': 'error',
                    'category': 'Custom Rule Error',
                    'message': f'Error evaluating rule {rule.name}: {str(e)}',
                    'recommendation': 'Review and fix the custom rule configuration'
                })
                
        return issues
    
    def _evaluate_condition(self, element: BeautifulSoup, condition: str) -> bool:
        """Evaluate a condition against an element."""
        # Basic conditions
        if condition == "exists":
            return True
        elif condition == "not_exists":
            return False
            
        # Attribute conditions
        if condition.startswith("has_attr:"):
            attr = condition.split(":")[1]
            return attr in element.attrs
            
        # Attribute value conditions
        if condition.startswith("attr_equals:"):
            attr, value = condition.split(":")[1].split("=")
            return element.get(attr) == value
            
        # Content conditions
        if condition.startswith("contains_text:"):
            text = condition.split(":")[1]
            return text.lower() in element.get_text().lower()
            
        # Regular expression conditions
        if condition.startswith("matches:"):
            pattern = condition.split(":")[1]
            return bool(re.search(pattern, str(element)))
            
        return False
