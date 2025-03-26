
# ✅ CI/CD & Code Quality – LMS Assessment

This project includes automated quality checks using **GitHub Actions** and standard Python tooling to ensure code consistency, reliability, and maintainability.

---

## 🚀 GitHub Actions CI Pipeline

Located at:
```
.github/workflows/python-ci.yml
```

### 🔁 When It Runs:
- On every `push` to the `main` branch
- On all `pull_request`s targeting `main`

---

## ✅ What It Checks

| Step                 | Tool     | Purpose                                 |
|----------------------|----------|-----------------------------------------|
| ✅ Linting           | flake8   | Enforces code style and catches errors |
| ✅ Unit Tests        | pytest   | Verifies API behavior and logic         |
| ⚙️ Type Checking     | mypy     | (Optional) Checks Python type hints     |
| ⚙️ Format Checking   | black    | (Optional) Ensures code style consistency |
| ⚙️ Security Linting  | bandit   | (Optional) Flags common security issues |

---

## 🧪 Run Quality Checks Locally

```bash
# Run lint check
flake8 app tests

# Run all tests
pytest

# (Optional) Check formatting
black . --check

# (Optional) Static type checking
mypy app

# (Optional) Security scan
bandit -r app
```

---

## 🧼 Notes

- Warnings from `mypy` are acknowledged; some are expected due to Pydantic + SQLAlchemy.
- Formatting and type checking are included for CI enrichment, but not enforced strictly.
- Logs are structured and sensitive info is excluded (e.g., tokens, passwords).
