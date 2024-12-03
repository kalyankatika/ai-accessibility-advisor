document.addEventListener('DOMContentLoaded', function() {
    // Load existing rules
    loadRules();
    
    // Handle form submission
    const form = document.getElementById('createRuleForm');
    if (form) {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            createRule();
        });
    }
});

function loadRules() {
    fetch('/custom-rules')
        .then(response => response.json())
        .then(rules => {
            const rulesList = document.getElementById('rulesList');
            rulesList.innerHTML = '';
            
            rules.forEach(rule => {
                const ruleElement = document.createElement('div');
                ruleElement.className = 'list-group-item';
                ruleElement.innerHTML = `
                    <div class="d-flex justify-content-between align-items-center">
                        <div>
                            <h3 class="h6 mb-1">${rule.name}</h3>
                            <p class="mb-1">${rule.description}</p>
                            <small class="text-muted">
                                Selector: ${rule.selector}<br>
                                Condition: ${rule.condition}
                            </small>
                        </div>
                        <button class="btn btn-danger btn-sm" onclick="deleteRule('${rule.name}')">
                            Delete
                        </button>
                    </div>
                `;
                rulesList.appendChild(ruleElement);
            });
        })
        .catch(error => console.error('Error loading rules:', error));
}

function createRule() {
    const formData = new FormData(document.getElementById('createRuleForm'));
    const data = Object.fromEntries(formData.entries());
    
    fetch('/custom-rules', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
    })
    .then(response => response.json())
    .then(result => {
        if (result.error) {
            alert(result.error);
        } else {
            document.getElementById('createRuleForm').reset();
            loadRules();
        }
    })
    .catch(error => {
        console.error('Error creating rule:', error);
        alert('Failed to create rule');
    });
}

function deleteRule(ruleName) {
    if (!confirm('Are you sure you want to delete this rule?')) {
        return;
    }
    
    fetch(`/custom-rules/${ruleName}`, {
        method: 'DELETE',
    })
    .then(response => response.json())
    .then(result => {
        if (result.error) {
            alert(result.error);
        } else {
            loadRules();
        }
    })
    .catch(error => {
        console.error('Error deleting rule:', error);
        alert('Failed to delete rule');
    });
}
