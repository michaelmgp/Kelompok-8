#!/bin/bash

echo "🔒 Backend Security Check"
echo "========================"

# Activate virtual environment if it exists
if [ -d ".venv" ]; then
    echo "🐍 Activating virtual environment..."
    source .venv/bin/activate
fi

# Check Python version
echo "🐍 Python version:"
python3 --version

echo ""

# Check pip version
echo "📦 pip version:"
pip --version

echo ""

# Check for outdated packages
echo "📦 Checking for outdated packages..."
pip list --outdated

echo ""

# Run security audit with pip-audit
echo "🔍 Running pip-audit (CVE scanner)..."
if command -v pip-audit &> /dev/null; then
    pip-audit
else
    echo "⚠️  pip-audit not installed. Installing..."
    pip install pip-audit
    pip-audit
fi

echo ""

# Run safety check
echo "🛡️  Running safety check..."
if command -v safety &> /dev/null; then
    safety check
else
    echo "⚠️  safety not installed. Installing..."
    pip install safety
    safety check
fi

echo ""

# Run bandit security linter
echo "🔍 Running bandit security linter..."
if command -v bandit &> /dev/null; then
    bandit -r . -f json -o bandit-report.json
    echo "📄 Bandit report saved to bandit-report.json"
else
    echo "⚠️  bandit not installed. Installing..."
    pip install bandit
    bandit -r . -f json -o bandit-report.json
    echo "📄 Bandit report saved to bandit-report.json"
fi

echo ""

echo "✅ Security check complete!"
echo ""
echo "To fix vulnerabilities:"
echo "  pip install --upgrade <package>  # Update specific package"
echo "  pip install -r requirements.txt  # Reinstall with updated versions"
echo "  pip-audit --fix                 # Auto-fix some issues"
echo ""
echo "Reports generated:"
echo "  - bandit-report.json (security linting)"
