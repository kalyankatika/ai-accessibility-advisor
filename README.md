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

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd <repository-name>
```

2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
Create a `.env` file with the following variables:
```
FLASK_SECRET_KEY=your-secret-key
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

## Contributing

1. Fork the repository
2. Create a feature branch
3. Submit a pull request

## License

[Insert License Information]
