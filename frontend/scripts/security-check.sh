#!/bin/bash

echo "🔒 Frontend Security Check"
echo "=========================="

# Check for outdated packages
echo "📦 Checking for outdated packages..."
npm outdated

echo ""

# Run security audit
echo "🔍 Running security audit..."
npm audit

echo ""

# Check for known vulnerabilities
echo "⚠️  Checking for known vulnerabilities..."
npm audit --audit-level=moderate

echo ""

# Check Node.js version
echo "🟢 Node.js version:"
node --version

echo ""

# Check npm version
echo "📦 npm version:"
npm --version

echo ""

echo "✅ Security check complete!"
echo ""
echo "To fix vulnerabilities:"
echo "  npm run security:fix          # Auto-fix safe issues"
echo "  npm run security:fix-force    # Force fix all issues"
echo "  npm run deps:update           # Update dependencies"
echo "  npm run deps:update-interactive # Interactive updates"
