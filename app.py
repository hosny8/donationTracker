from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///donations.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Donation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    donor = db.Column(db.String(100), nullable=False)
    donation_type = db.Column(db.String(10), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    donation_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

with app.app_context():
    db.create_all()



@app.route('/donations', methods=['GET'])
def get_donations():
    donations = Donation.query.all()
    return jsonify([{
        'id': d.id,
        'donor': d.donor,
        'amount': d.amount,
        'donation_type': d.donation_type,
        'donation_date': d.donation_date.strftime('%Y-%m-%d')
    } for d in donations])

@app.route('/donation', methods=['POST'])
def add_donation():
    data = request.get_json()

    if "donor" not in data or "donation_type" not in data or "amount" not in data:
        return jsonify({"error": "Missing fields"}), 400

    donation = Donation(
        donor=data['donor'],
        donation_type=data['donation_type'],
        amount=data['amount']
    )
    db.session.add(donation)
    db.session.commit()

    return jsonify({"message": "Donation added successfully!"}), 201

@app.route('/donation/<int:id>', methods=['DELETE'])
def delete_donation(id):
    donation = Donation.query.get_or_404(id)
    db.session.delete(donation)
    db.session.commit()

    return jsonify({
        "message": "Donation deleted successfully!",
        "deleted": {
            "id": donation.id,
            "donor": donation.donor,
            "donation_type": donation.donation_type,
            "amount": donation.amount
        }
    }), 200

@app.route('/donations/total', methods=['GET'])
def total_donations():
    total = Donation.query.count()
    return jsonify({"total_donations": total}), 200

@app.route('/donations/total/USD', methods=['GET'])
def total_donations_usd():
    total = Donation.query.filter_by(donation_type='USD').count()
    return jsonify({"total_usd_donations": total}), 200

@app.route('/donations/total/EURO', methods=['GET'])
def total_donations_euro():
    total = Donation.query.filter_by(donation_type='EURO').count()
    return jsonify({"total_euro_donations": total}), 200

@app.route('/donations/donor/<donor>', methods=['GET'])
def find_donation_by_donor(donor):
    donations = Donation.query.filter_by(donor=donor).all()
    return jsonify({
        "total_by_donor": len(donations),
        "donations": [{
            'id': d.id,
            'amount': d.amount,
            'donation_type': d.donation_type,
            'donation_date': d.donation_date.strftime('%Y-%m-%d')
        } for d in donations]
    }), 200

@app.route('/donations/top/<int:n>', methods=['GET'])
def get_top_donors(n):
    donations = Donation.query.all()
    top_donors = {}
    
    for donation in donations:
        if donation.donor in top_donors:
            top_donors[donation.donor] += donation.amount
        else:
            top_donors[donation.donor] = donation.amount

    sorted_donors = dict(sorted(top_donors.items(), key=lambda x: x[1], reverse=True)[:n])
    return jsonify({"top donors": sorted_donors}), 200

@app.route('/donations', methods=['DELETE'])
def clear_donations():
    num_deleted = Donation.query.delete()
    db.session.commit()
    return jsonify({"message": "All donations deleted successfully!", "count": num_deleted}), 200

@app.route('/donations/date_range', methods=['GET'])
def donations_in_date_range():
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    if not start_date or not end_date:
        return jsonify({"error": "Both start_date and end_date are required"}), 400
    
    try:
        start = datetime.strptime(start_date, '%Y-%m-%d')
        end = datetime.strptime(end_date, '%Y-%m-%d')
    except ValueError:
        return jsonify({"error": "Invalid date format. Use YYYY-MM-DD"}), 400

    donations = Donation.query.filter(
        Donation.donation_date >= start,
        Donation.donation_date <= end
    ).all()

    return jsonify([{
        'id': d.id,
        'donor': d.donor,
        'amount': d.amount,
        'donation_type': d.donation_type,
        'donation_date': d.donation_date.strftime('%Y-%m-%d')
    } for d in donations]), 200

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
