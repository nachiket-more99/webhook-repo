# webhook-repo

## Features

- Shows who pushed, created PR, or merged a branch
- Updates every 15 seconds
- Stores events in MongoDB

## Setup

1. Clone the repo:
```bash
git clone <repo-url>
cd webhook-repo
```
2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```
3. Install dependencies:
```bash
pip install -r requirements.txt
```
4. Set MongoDB URI:
```bash
export MONGO_URI="your-mongodb-uri"
```
5. Run Flask:
```bash
python run.py
```
6. For GitHub webhooks, use ngrok to expose your local server:
```bash
ngrok http 5000
```

## Usage
- Open http://127.0.0.1:5000/
- Do Push / PR / Merge on your GitHub repo
- Events appear on the page in order