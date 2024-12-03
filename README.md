# AI-Powered Web Accessibility Testing Platform

An enterprise-grade web accessibility testing platform that uses AI to evaluate web pages for accessibility compliance and FDS design specifications.

## Features

- WCAG 2.1 compliance checking
- Color contrast validation
- FDS design specification verification
- Detailed accessibility reports
- Batch URL processing (coming soon)
- Custom accessibility rule creation (coming soon)
- Historical analysis tracking (coming soon)

## Deployment

### Vercel Deployment

1. Install Vercel CLI:
```bash
npm i -g vercel
```

2. Login to Vercel:
```bash
vercel login
```

3. Configure the following environment variables in your Vercel project settings:
   - `FLASK_SECRET_KEY`: Your Flask secret key
   - `DATABASE_URL`: PostgreSQL database URL (if using a single connection URL)
   - Or individual PostgreSQL connection variables:
     - `PGHOST`: Database host
     - `PGPORT`: Database port
     - `PGDATABASE`: Database name
     - `PGUSER`: Database user
     - `PGPASSWORD`: Database password

4. Deploy to Vercel:
```bash
vercel
```

5. For production deployment:
```bash
vercel --prod
```

## Installation

### Prerequisites
- Python 3.11 or higher
- pip package manager

### Steps

1. Clone the repository:
```bash
git clone https://github.com/kalyankatika/ai-accessibility-advisor.git
cd ai-accessibility-advisor
```

2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
Create a `.env` file in the root directory with the following variables:
```ini
# Required
FLASK_SECRET_KEY=your-secret-key-here

# Optional
FLASK_ENV=development
DEBUG=True
```

## Usage

1. Start the Flask server:
```bash
python main.py
```

2. Open your browser and navigate to:
```
http://localhost:5000
```

3. Enter a URL to analyze and receive a detailed accessibility report.

## API Documentation

### Endpoints

#### POST /analyze
Analyzes a webpage for accessibility issues.

**Request Format:**
```json
{
  "url": "https://example.com"
}
```

**Response Format:**
```json
{
  "accessibility": [
    {
      "type": "error|warning",
      "category": "string",
      "message": "string",
      "recommendation": "string"
    }
  ],
  "colors": [
    {
      "type": "error|warning",
      "category": "string",
      "message": "string",
      "recommendation": "string"
    }
  ],
  "url": "string"
}
```

## Testing

### Running Tests
1. Install test dependencies:
```bash
pip install pytest pytest-cov
```

2. Run the test suite:
```bash
pytest tests/
```

3. Generate coverage report:
```bash
pytest --cov=./ tests/
```

### Adding New Tests
1. Create test files in the `tests/` directory
2. Follow the naming convention: `test_*.py`
3. Use pytest fixtures for common setup
4. Include both unit tests and integration tests
5. Ensure proper mocking of external services

## Contributing

We welcome contributions! Please follow these steps:

1. Fork the repository
2. Create a feature branch:
```bash
git checkout -b feature/your-feature-name
```

3. Follow our coding standards:
   - Use PEP 8 style guide for Python code
   - Include docstrings for all functions and classes
   - Add type hints to function parameters
   - Write unit tests for new features

4. Commit your changes:
```bash
git commit -m "feat: add your feature description"
```

5. Push to your fork:
```bash
git push origin feature/your-feature-name
```

6. Submit a pull request

### Pull Request Guidelines
- Provide a clear description of the changes
- Include any relevant issue numbers
- Ensure all tests pass
- Update documentation as needed

## Color Validation

The platform implements comprehensive color validation including:
- WCAG 2.1 color contrast checking
- Text color validation against backgrounds
- Contrast ratio calculations
- FDS color palette compliance

## Development

The project uses Flask for the backend and Bootstrap for the frontend. Key components:

- `app.py`: Main Flask application
- `utils/`: Utility modules for accessibility checking
  - `accessibility_checker.py`: Core accessibility validation
  - `color_validator.py`: Color contrast and FDS compliance checking
  - `html_parser.py`: HTML content extraction

## Dependencies

- Flask: Web framework
- BeautifulSoup4: HTML parsing
- Trafilatura: Web content extraction
- SQLAlchemy: Database ORM (for future features)

## License

MIT License

Copyright (c) 2024

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
