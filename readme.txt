🧪 Getting Started (Local Demo)
1️⃣ Create & Activate Virtual Environment
python -m venv venv

Activate the environment:

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate

Install dependencies:

pip install -r requirements.txt
2️⃣ Start Backend (Django + Channels)

Navigate to backend directory:

cd backend

Create database tables (first time only):

python manage.py makemigrations
python manage.py migrate

Load demo data
(customers must be loaded before accounts):

python manage.py loaddata demo_customers

Create admin user:

python manage.py createsuperuser

Start ASGI server using Daphne:

daphne -b 127.0.0.1 -p 8000 backend.asgi:application

Backend server:

http://127.0.0.1:8000
3️⃣ Start Frontend Dashboard

Open a new terminal window:

cd frontend
python -m http.server 8001

Frontend dashboard:

http://127.0.0.1:8001
📤 Submit Transactions (Fraud Detection Demo)

Transactions are submitted via API:

POST http://127.0.0.1:8000/transaction/post/

Request body must be a JSON array

🟢 Safe Transaction Example
[
  {
    "sender_acc": "ADEMO001",
    "receiver_acc": "ADEMO002",
    "amount": 500.00,
    "location": "Kuala Lumpur, MY",
    "device_info": "Android Phone (Chrome 120)",
    "transaction_type": "TRANSFER"
  }
]
🔴 Fraud-like Transaction Example
[
  {
    "sender_acc": "ADEMO001",
    "receiver_acc": "ADEMO999",
    "amount": 9800.00,
    "location": "Moscow, RU",
    "device_info": "Unknown Android Device",
    "transaction_type": "TRANSFER"
  }
]
🟡 Mixed Batch (Safe + Fraud)
[
  {
    "sender_acc": "ADEMO002",
    "receiver_acc": "ADEMO003",
    "amount": 30.00,
    "location": "Subang Jaya, MY",
    "device_info": "Samsung Galaxy S22",
    "transaction_type": "TRANSFER"
  },
  {
    "sender_acc": "ADEMO002",
    "receiver_acc": "ADEMO888",
    "amount": 12000.00,
    "location": "Berlin, DE",
    "device_info": "Windows PC (Chrome)",
    "transaction_type": "TRANSFER"
  }
]
📊 Real-Time Demo Flow

Submit transaction data via API

Open frontend dashboard (http://127.0.0.1:8001)

New transactions appear instantly via WebSocket

Fraud transactions generate alerts automatically

Click Alert → Review to update alert status:

Confirm Fraud

False Positive
