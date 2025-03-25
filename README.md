Donation Tracker API

Overview

The Donation Tracker is a Flask-based web API that allows users to track and manage donations efficiently. The API supports operations such as adding, retrieving, and deleting donations, as well as aggregating totals based on donor, currency type, and date range. The backend is implemented in Python using Flask, and unit tests ensure the reliability of core functionalities. A user interface is planned for development and deployment in the final phase.

Features

Add Donations: Users can submit donations with details such as donor name, donation amount, and currency type.

Retrieve Donations: Users can fetch all donations or filter them based on donor name, currency, or date range.

Delete Donations: Donations can be deleted using their unique identifier.

Aggregate Totals: The API can compute the total donations made in different currencies or by specific donors.

Unit Testing: Python unit tests validate API endpoints to ensure correctness and stability.

Installation

Prerequisites

Python 3.x

Flask

Virtual environment (optional but recommended)

Setup Instructions

Clone the repository:

git clone <repository_url>
cd donation-tracker

Create and activate a virtual environment:

python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`

Install dependencies:

pip install -r requirements.txt

Run the Flask app:

python app.py

The API will be accessible at http://127.0.0.1:5000/

API Endpoints

1. Add a Donation

Endpoint: POST /donation

Request Body (JSON):

{
  "donor": "Alice",
  "donation_type": "USD",
  "amount": 50
}

Response:

{
  "message": "Donation added successfully!",
  "donation": {
    "id": 1,
    "donor": "Alice",
    "donation_type": "USD",
    "amount": 50
  }
}

2. Retrieve Donations

Endpoint: GET /donations

Query Parameters (Optional): donor, donation_type, start_date, end_date

Response:

[
  {
    "id": 1,
    "donor": "Alice",
    "donation_type": "USD",
    "amount": 50
  }
]

3. Delete a Donation

Endpoint: DELETE /donation/<donation_id>

Response:

{
  "message": "Donation deleted successfully!"
}

Running Tests

To ensure that the API works correctly, run the unit tests:

pytest test_donation_tracker.py


