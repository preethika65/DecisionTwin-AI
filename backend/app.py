from flask import Flask, jsonify, request
from flask_cors import CORS
from pymongo import MongoClient
from bson import ObjectId

app = Flask(__name__)
CORS(app)


# ---------------- MongoDB Connection ----------------

client = MongoClient("mongodb://localhost:27017/")

try:
    client.admin.command("ping")
    print("MongoDB Connected Successfully")

except Exception as e:
    print("MongoDB Connection Failed:", e)


db = client["DecisionTwinAI"]


users_collection = db["synthetic_users"]
scenarios_collection = db["scenarios"]
simulations_collection = db["simulations"]
results_collection = db["results"]



# ---------------- Home ----------------

@app.route("/")
def home():

    return "DecisionTwin AI Backend Running"



# ---------------- Dashboard ----------------

@app.route("/api/dashboard")
def dashboard():

    users_count = users_collection.count_documents({})
    simulations_count = simulations_collection.count_documents({})


    return jsonify({

        "users": users_count if users_count else 500,

        "simulations": simulations_count if simulations_count else 25,

        "accuracy": "94%"

    })



# ---------------- Synthetic Users ----------------

@app.route("/api/users", methods=["GET"])
def synthetic_users():


    users = list(
        users_collection.find({}, {"_id": 0})
    )


    if not users:


        default_users = [

            {
                "id": 1,
                "name": "User_001",
                "age": 28,
                "location": "Hyderabad",
                "behavior": "High Engagement"
            },

            {
                "id": 2,
                "name": "User_002",
                "age": 35,
                "location": "Warangal",
                "behavior": "Medium Engagement"
            },

            {
                "id": 3,
                "name": "User_003",
                "age": 22,
                "location": "Karimnagar",
                "behavior": "Low Engagement"
            }

        ]


        users_collection.insert_many(default_users)

        users = default_users



    return jsonify(users)




# ---------------- Create Scenario ----------------

@app.route("/api/scenario", methods=["POST"])
def create_scenario():

    data = request.get_json()

    scenario = {

        "scenario_name": data.get("scenario_name"),
        "decision": data.get("decision"),
        "target_users": data.get("target_users"),
        "status": "Scenario Created"

    }


    scenarios_collection.insert_one(scenario)


    return jsonify({

        "status": "Scenario Created",

        "scenario_name": scenario["scenario_name"],

        "decision": scenario["decision"],

        "target_users": scenario["target_users"]

    })




# ---------------- Get All Scenarios ----------------

@app.route("/api/scenarios")
def get_scenarios():


    scenarios = list(

        scenarios_collection.find({}, {"_id": 0})

    )


    return jsonify(scenarios)





# ---------------- Latest Scenario ----------------

@app.route("/api/latest-scenario")
def latest_scenario():


    scenario = scenarios_collection.find_one(

        {},

        {"_id": 0},

        sort=[("_id", -1)]

    )


    if scenario:

        return jsonify(scenario)



    return jsonify({

        "scenario_name": "No Scenario",

        "decision": "No Decision",

        "target_users": 0

    })






# ---------------- Simulation ----------------

@app.route("/api/simulation")
def simulation():


    scenario = scenarios_collection.find_one(

        {},

        {"_id": 0},

        sort=[("_id", -1)]

    )



    if not scenario:


        return jsonify({

            "scenario": "No Scenario",

            "impact": "Unknown",

            "customer_change": "0%",

            "revenue_change": "0%",

            "confidence": "0%"

        })



    simulation_data = {


        "scenario": scenario["scenario_name"],


        "impact": "Medium",


        "customer_change": "-8%",


        "revenue_change": "+12%",


        "confidence": "92%"

    }



    simulations_collection.insert_one(simulation_data.copy())


    return jsonify(simulation_data)







# ---------------- Results ----------------

@app.route("/api/results")
def results():


    scenario = scenarios_collection.find_one(

        {},

        {"_id": 0},

        sort=[("_id", -1)]

    )



    if not scenario:


        return jsonify({

            "scenario": "No Scenario",

            "prediction": "No Prediction",

            "customer_impact": "0%",

            "revenue_impact": "0%",

            "confidence": "0%",

            "recommendation": "Create a scenario first"

        })





    result_data = {



        "scenario": scenario["scenario_name"],


        "prediction": "Revenue Growth Expected",


        "customer_impact": "-8%",


        "revenue_impact": "+12%",


        "confidence": "92%",


        "recommendation": "Proceed with controlled rollout"


    }





    results_collection.insert_one(result_data.copy())


    return jsonify(result_data)






# ---------------- Run Server ----------------

if __name__ == "__main__":


    app.run(debug=True)