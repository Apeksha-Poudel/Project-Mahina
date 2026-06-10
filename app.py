from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient

app = Flask(__name__)
CORS(app)

client = MongoClient(
    "mongodb+srv://poudelapeksha65_db_user:mahina123@projectmahina.feoyx2e.mongodb.net/?appName=Projectmahina"
)

# ✅ Ping test goes HERE — before app.run()
try:
    client.admin.command('ping')
    print("✅ MongoDB connected!")
except Exception as e:
    print("❌ MongoDB connection failed:", e)

db = client["Project_mahina"]
donations = db["donation_data"]

@app.route("/donate", methods=["POST"])
def donate():
    try:
        data = request.json
        print("📥 Received:", data)  # see what's coming in
        donations.insert_one({
            "name": data["name"],
            "email": data["email"],
            "amount": data["amount"],
            "date": data["date"]
        })
        print("✅ Inserted successfully!")
        return jsonify({"success": True})
    except Exception as e:
        print("❌ Insert failed:", e)
        return jsonify({"error": str(e)}), 500

@app.route("/donations", methods=["GET"])
def get_donations():
    all_donations = list(donations.find({}, {"_id": 0}))
    return jsonify(all_donations)

if __name__ == "__main__":
    app.run(debug=True)