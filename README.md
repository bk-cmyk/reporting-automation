# KPI Bullet Summarizer

A lightweight API service that:

1. Accepts report uploads (CSV or Excel files containing performance tables).
2. Returns key KPI insights as concise bullet points.
3. Sends those bullets through email.

## Features

- **Upload and summarize:** `POST /summarize`
- **Email bullets:** `POST /email`
- **Health check:** `GET /health`

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## API usage

### Summarize a report file

```bash
curl -X POST "http://127.0.0.1:8000/summarize" \
  -F "file=@sample_report.csv"
```

Response:

```json
{
  "filename": "sample_report.csv",
  "bullets": [
    "Revenue: latest value is 145000.00, up 8.00% vs the previous data point.",
    "ConversionRate: latest value is 3.20, down 1.54% vs the previous data point.",
    "Overall strongest latest metric: Revenue at 145000.00."
  ]
}
```

### Send bullets by email

```bash
curl -X POST "http://127.0.0.1:8000/email" \
  -H "Content-Type: application/json" \
  -d '{
    "to": ["stakeholder@example.com"],
    "subject": "Weekly KPI Summary",
    "bullets": [
      "Revenue increased 8% week-over-week.",
      "Churn improved by 0.4 points."
    ]
  }'
```

## Environment variables

### Email (required for `/email`)

- `SMTP_HOST` (e.g. `smtp.gmail.com`)
- `SMTP_PORT` (e.g. `587`)
- `SMTP_USERNAME`
- `SMTP_PASSWORD`
- `SMTP_USE_TLS` (`true`/`false`, default `true`)
- `EMAIL_FROM` (sender address)

## Notes

- This implementation focuses on **table-based reports** (`.csv`, `.xlsx`, `.xls`).
- If you want chart-image interpretation, you can extend `ReportSummarizer` with OCR/vision or an LLM vision model.
