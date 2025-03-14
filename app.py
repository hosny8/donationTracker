from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///donations.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Donation(db.model):
    id = db.Column(db.Integer, primary_key=True)
    donor = db.Column(db.String(100), nullable=False)
    donation_type = db.Column(db.String(10), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    donation_date = db.Column(db.Datetime, datetime.utcnow)

@app.before_first_request
def create_tables():
    db.create_all()

donations = []

@app.route('/donations', methods=['GET'])
def get_donations():
    donations = Donation.query.all()
    return jsonify([{'id': d.id, 'donor': d.donor, 'amount': d.amount, 'donation_type': d.donation_type, 'donation_date': d.donation_date}.strftime('%Y-%m-%d') for d in donations])
     

@app.route('/donation', methods=['POST'])
def add_donation(donor, donation_type, amount):
    data = request.get_json()

    if "donor" not in data or "donation_type" not in data or "amount" not in data:
        return jsonify({"error": "Missing fields"}), 400

    donation = Donation(
        id=data['id'],
        donor=data['donor'],
        donation_type=data['donation_type'],
        amount=data['amount'],
        donation_date=data['donation_date']
    )
    db.session.add(donation)
    db.session.commit()

    return jsonify({"message": "Donation added successfully!"}), 201


@app.route('/donation/<int:index>', methods=['DELETE'])
def delete_donation(id):
    donation = Donation.queury.get(id)
    if id < 0 or id >= len(donations):
        return jsonify({"error": "Invalid index"}), 400

    db.session.delete(donation)
    db.session.commit()

    return jsonify({"message": "Donation deleted successfully!", "deleted": delete_donation}), 200

@app.route('/donations/total', methods=['GET'])
def total_donations():
    total = 0
    for donation in donations:
        total += donation['amount']

    return jsonify({"total_donations": total}), 200

@app.route('/donations/total/USD', methods=['GET'])
def total_donations_usd():
    total = 0
    for donation in donations:
        if donation['donation_type'] == "USD":
            total += donation['amount']

    return jsonify({"total_usd_donations": total}), 200

@app.route('/donations/total/EURO', methods=['GET'])
def total_donations_euro():
    total = 0
    for donation in donations:
        if donation['donation_type'] == "EURO":
            total += donation['amount']

    return jsonify({"total_euro_donations": total}), 200

@app.route('/donations/donor/<donor>', methods=['GET'])
def find_donation_by_donor(donor):
    total = 0
    for donation in donations:
        if donation['donor'] == donor:
            total += donation['amount']

    return jsonify({"total_by_donor": total}), 200


@app.route('/donations/top/<int:n>', methods=['GET'])
def getTopDonors(n):
    top_donors = {}
    for donation in donations:
        if donation['donor'] in top_donors:
            top_donors[donation['donor']] += donation['amount']
        else:
            top_donors[donation['donor']] = donation['amount']

    sorted_top_donors = sorted(top_donors.items(), key=lambda x: x[1], reverse=True)[:n]
    top_donors = dict(list(sorted_top_donors.items())[n:])
    return jsonify({"top donors": top_donors}), 200
    


@app.route('/donations/top/<int:n>', methods=['DELETE'])
def delete_request(n):
    donations.clear()
    return jsonify({"message": "All donations deleted"}), 200 


@app.route('/donations/date_range', methods=['GET'])
def donations_in_date_range():
    donation_total_date = []
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')


    try:
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
        end_date = datetime.strptime(end_date, '%Y-%m-%d')
    except:
        return jsonify({"error"})
   
   
    for donation in donations:
        donation_date = datetime.strptime(donation['donation_date'], '%Y-%m-%d')
        if start_date <= donation_date <= end_date:
            donation_total_date.append(donation)
   
   
    return jsonify({"These are the donations in the date range: " : donation_total_date}), 200

@app.route('/donations/date_range', methods=['GET'])
def donations_in_date_range_USD():
    donation_total_date = []
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')


    try:
         start_date = datetime.strptime(start_date, '%Y-%m-%d')
         end_date = datetime.strptime(end_date, '%Y-%m-%d')
    except:
        return jsonify({"error"})
   
   
    for donation in donations:
        donation_date = datetime.strptime(donation['donation_date'], '%Y-%m-%d')
        if start_date <= donation_date <= end_date:
            if donation["donation_type"] == "USD":
                donation_total_date.append(donation['amount'])
               

    total = sum(donation_total_date)

   
    return jsonify({"This is the total amount of donations in this date range: " : total}), 200          
           

  

if __name__ == '__main__':
    app.run(debug=True)