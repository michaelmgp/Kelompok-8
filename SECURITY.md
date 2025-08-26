# 🔒 Security Guide

This document outlines security best practices and tools for the Web3 Job Agent Platform.

## 🚨 Security Scanning

### Frontend (Node.js)

```bash
cd frontend

# Run security audit
npm run security:audit

# Fix vulnerabilities automatically
npm run security:fix

# Check for outdated packages
npm run deps:check

# Update dependencies
npm run deps:update

# Interactive dependency updates
npm run deps:update-interactive
```

### Backend (Python)

```bash
cd ai_chatbot

# Run security check script
chmod +x scripts/security-check.sh
./scripts/security-check.sh

# Or run individual tools
pip install pip-audit safety bandit
pip-audit
safety check
bandit -r .
```

## 🛡️ Security Tools

### Frontend
- **npm audit** - Built-in vulnerability scanner
- **npm-check-updates** - Dependency update checker
- **Snyk** - Advanced security scanning (optional)

### Backend
- **pip-audit** - CVE vulnerability scanner
- **safety** - Security vulnerability checker
- **bandit** - Security linter for Python
- **pip-tools** - Dependency management (optional)

## 🔍 Common CVE Fixes

### Node.js Dependencies
```bash
# Update specific vulnerable package
npm update <package-name>

# Force update all packages
npm update --force

# Install latest versions
npm install <package-name>@latest
```

### Python Dependencies
```bash
# Update specific package
pip install --upgrade <package-name>

# Update all packages
pip list --outdated | cut -d ' ' -f1 | xargs -n1 pip install -U

# Use pip-audit to fix
pip-audit --fix
```

## 📊 Security Reports

### Frontend
- `npm audit --json` - JSON format for CI/CD
- `npm outdated` - Outdated package list

### Backend
- `bandit-report.json` - Security linting report
- `pip-audit` output - CVE findings
- `safety check` output - Vulnerability details

## 🚀 CI/CD Integration

### GitHub Actions Example
```yaml
name: Security Scan
on: [push, pull_request]

jobs:
  security:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Frontend Security
        run: |
          cd frontend
          npm ci
          npm audit --audit-level=moderate
          
      - name: Backend Security
        run: |
          cd ai_chatbot
          pip install -r requirements.txt
          pip-audit
          bandit -r . -f json
```

## 🔧 Dependency Pinning

### Frontend
- Use `package-lock.json` for exact versions
- Consider using `npm ci` in production
- Regular `npm audit` checks

### Backend
- Pin versions in `requirements.txt`
- Use `pip-tools` for dependency compilation
- Regular `pip-audit` checks

## 📈 Security Monitoring

### Regular Checks
- **Weekly**: Run security scans
- **Monthly**: Update dependencies
- **Quarterly**: Review security policies

### Automated Alerts
- GitHub Dependabot alerts
- npm audit notifications
- pip-audit CI/CD failures

## 🚨 Emergency Response

### Critical Vulnerabilities
1. **Immediate**: Stop affected services
2. **Assessment**: Evaluate impact
3. **Fix**: Update or patch dependencies
4. **Test**: Verify fixes work
5. **Deploy**: Restart services
6. **Monitor**: Watch for issues

### Contact
- **Security Issues**: Create GitHub issue with [SECURITY] tag
- **Critical CVEs**: Immediate response required
- **Dependencies**: Regular maintenance schedule

## 📚 Resources

- [npm Security](https://docs.npmjs.com/about-audit-reports)
- [pip-audit](https://github.com/pypa/pip-audit)
- [Bandit](https://bandit.readthedocs.io/)
- [Safety](https://pyup.io/safety/)
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)

---

**Remember: Security is an ongoing process, not a one-time task!** 🔒
