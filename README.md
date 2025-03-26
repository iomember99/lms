
# 📊 Credable LMS – Loan Management System (Technical Assessment)

This is a lightweight Loan Management System (LMS) built as part of a technical assessment. It handles:

- Customer subscription
- Loan request handling
- Integration with banking systems (via SOAP)
- Integration with a scoring engine (via REST)
- Scoring decision logic (mocked)
- Secure transaction exposure
- Structured logging and clean architecture

---

## 🚀 Tech Stack

- **Python 3.11+**
- **FastAPI** – REST API
- **SQLAlchemy + SQLite** – Lightweight database
- **Zeep** – SOAP client (mocked for KYC & transactions)
- **httpx** – Async REST client (mocked for scoring engine)
- **Pydantic** – Data validation and request parsing
- **Docker** (optional) – Deployment packaging
- **Ngrok** – Expose local services for scoring callback testing

🧹 **Dev Tip:** To reset the database, simply delete the `loans.db` file:

```bash
rm loans.db
```

---

## 🔧 Core Functionalities

### ✅ /subscribe
Registers a new customer using their customer number.

### ✅ /loan
Handles loan requests:
- Validates customer
- Prevents duplicates
- Fetches KYC and transaction data (mocked)
- Registers LMS endpoint with scoring engine (mocked)
- Initiates scoring (mocked)
- Polls for result and makes decision

### ✅ /status/'{{customerNumber}}'
Returns the latest loan status for a given customer.

### ✅ /transactions/'{{customerNumber}}'
Exposes transaction data for a customer (for scoring engine).
- Protected with Basic Auth
- Returns data fetched from the core banking system (mocked)

---

## 🔐 Authentication

| Endpoint                           | Protection  |
|-----------------------------------|-------------|
| /transactions/{{customerNumber}}  | ✅ Basic Auth |

Credentials from `.env`:
```
CLIENT_USERNAME=lmsuser
CLIENT_PASSWORD=lmspass
```

---

## ⚠️ Mocked Integrations

Due to persistent failures reaching the provided test endpoints (*.credable.io), the following external integrations are mocked:

| External Service            | Mocked? | Notes                                |
|-----------------------------|---------|--------------------------------------|
| CBS KYC (SOAP)              | ✅       | WSDL points to unreachable endpoint  |
| CBS Transactions (SOAP)     | ✅       | Same as above                        |
| Scoring Registration        | ✅       | Endpoints unreachable or broken      |
| Scoring API (initiate/query)| ✅       | Endpoints unreachable or broken      |

---

## 🧪 Sample API Flow

### 1. Subscribe a Customer
```http
POST /subscribe
Content-Type: application/json
{
  "customer_number": "234774784"
}
```

### 2. Request a Loan
```http
POST /loan
Content-Type: application/json
{
  "customer_number": "234774784",
  "amount": 1000
}
```

### 3. Check Loan Status
```http
GET /status/234774784
```

### 4. Scoring Engine Callback for Transactions
```http
GET /transactions/234774784
Authorization: Basic (lmsuser / lmspass)
```

---

## 🛠 Environment Setup

Create a `.env` file with:

```
DATABASE_URL=sqlite:///./loans.db
SCORING_BASE_URL=https://scoringtest.credable.io/api/v1
CORE_BANKING_USERNAME=admin
CORE_BANKING_PASSWORD=pwd123
CLIENT_NAME=CredableLMS
CLIENT_USERNAME=lmsuser
CLIENT_PASSWORD=lmspass
RETRY_LIMIT=3
```

---

## 📦 Local Development

```bash
git clone <repo-url>
cd loan-lms
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

---

## 🐳 Running with Docker

You can run the entire app in a container using Docker:

### 🔨 Build the Docker image:

```bash
docker build -t lms-app .
```

### ▶️ Run the container:

```bash
docker run -p 8000:8000 lms-app
```

### ⚙️ Optional: Load environment variables from `.env`:

```bash
docker run --env-file .env -p 8000:8000 lms-app
```

Once running, access the API at:
```
http://localhost:8000/docs
```

---

➡️ [See full CI/CD & Code Quality guide](CI_CD.md)

---

## 📁 Project Structure

```
app/
├── api/
├── core/
├── models/
├── utils/
└── main.py
logs/
|-- app.log
tests/
```

---

## 👨‍💻 Developer

**David Mwangi**  
DevOps Engineer – M-Pesa Africa  
📧 dmwangit@gmail.com  
📞 0701588368

> Due to unavailable external endpoints, all integrations (KYC, transactions, scoring) are mocked while preserving full logic and architecture.
