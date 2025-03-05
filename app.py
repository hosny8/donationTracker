from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)



donations = []

@app.route('/donations', methods=['GET'])
def get_donations():
    return jsonify(donations), 200

@app.route('/donation', methods=['POST'])
def add_donation(donor, donation_type, amount):
    data = request.get_json()

    if "donor" not in data or "donation_type" not in data or "amount" not in data:
        return jsonify({"error": "Missing fields"}), 400

    donation = {
        'donor': data['donor'],
        'donation_type': data['donation_type'],
        'amount': data['amount']
    }

    donations.append(donation)

    return jsonify({"message": "Donation added successfully!"}), 201

@app.route('/donation/<int:index>', methods=['DELETE'])
def delete_donation(index):
    if index < 0 or index >= len(donations):
        return jsonify({"error": "Invalid index"}), 400

    deleted_donation = donations.pop(index)

    return jsonify({"message": "Donation deleted successfully!", "deleted": deleted_donation}), 200

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

    # Try to convert the string dates to actual date objects
    try:
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d')
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

    # Try to convert the string dates to actual date objects
    try:
         start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
         end_date = datetime.strptime(end_date_str, '%Y-%m-%d')
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