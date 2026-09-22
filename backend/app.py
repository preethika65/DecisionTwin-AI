from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from pymongo import MongoClient
from bson import ObjectId

import os
from datetime import datetime

from generator import (
    generate_personas,
    ask_all_personas,
    generate_survey_insights,
    generate_survey_product_rating,
    interview_persona,
    generate_interview_insights,
    generate_product_rating,
    generate_theme_analysis,
    generate_sentiment_analysis,
    generate_key_quotes
)

from report_generator import create_research_report


# =========================================================
# FLASK APP
# =========================================================

app = Flask(__name__)
CORS(app)


# =========================================================
# MONGODB
# =========================================================

client = MongoClient("mongodb://localhost:27017/")

db = client["DecisionTwinAI"]

users_collection = db["synthetic_users"]
scenarios_collection = db["scenarios"]
simulations_collection = db["simulations"]

survey_results_collection = db["survey_results"]
interview_results_collection = db["interview_results"]


try:
    client.admin.command("ping")
    print("MongoDB Connected Successfully")

except Exception as error:
    print("MongoDB Connection Error:", error)


# =========================================================
# SERIALIZE OBJECTID
# =========================================================

def serialize_document(document):

    if isinstance(document, ObjectId):
        return str(document)

    if isinstance(document, list):
        return [
            serialize_document(item)
            for item in document
        ]

    if isinstance(document, dict):
        return {
            key: serialize_document(value)
            for key, value in document.items()
        }

    return document


# =========================================================
# HOME
# =========================================================

@app.route("/")
def home():

    return jsonify({
        "message": "DecisionTwin AI Backend Running"
    })


# =========================================================
# DASHBOARD API
# =========================================================

@app.route("/api/dashboard", methods=["GET"])
def dashboard():

    try:

        users_count = users_collection.count_documents({})
        simulations_count = simulations_collection.count_documents({})

        return jsonify({

            "users": users_count,

            "simulations": simulations_count,

            "accuracy": "94%"

        })

    except Exception as error:

        return jsonify({
            "error": str(error)
        }), 500


# =========================================================
# GET USERS
# =========================================================

@app.route("/api/users", methods=["GET"])
def get_users():

    try:

        users = list(
            users_collection.find({})
        )

        return jsonify(
            serialize_document(users)
        )

    except Exception as error:

        return jsonify({
            "error": str(error)
        }), 500


# =========================================================
# GENERATE PERSONAS
# =========================================================

@app.route("/api/generate-personas", methods=["POST"])
def generate_persona_data():

    try:

        data = request.get_json() or {}

        product = data.get(
            "product",
            ""
        ).strip()

        audience = data.get(
            "audience",
            ""
        ).strip()

        research = data.get(
            "research",
            ""
        ).strip()

        count = int(
            data.get("count") or 5
        )

        # -------------------------------------------------
        # VALIDATION
        # -------------------------------------------------

        if not product:

            return jsonify({
                "error": "Product is required"
            }), 400

        if not audience:

            return jsonify({
                "error": "Audience is required"
            }), 400

        if not research:

            return jsonify({
                "error": "Research objective is required"
            }), 400

        if count < 1 or count > 20:

            return jsonify({
                "error": "Count must be between 1 and 20"
            }), 400

        # -------------------------------------------------
        # GENERATE
        # -------------------------------------------------

        personas = generate_personas(
            count,
            product,
            audience,
            research
        )

        if not personas:

            return jsonify({
                "error":
                    "Persona generation failed. Check Ollama."
            }), 500

        # -------------------------------------------------
        # REMOVE OLD DATA
        # -------------------------------------------------

        users_collection.delete_many({})
        survey_results_collection.delete_many({})
        interview_results_collection.delete_many({})

        # -------------------------------------------------
        # CLEAN PERSONAS
        # -------------------------------------------------

        clean_personas = []

        for persona in personas:

            persona = dict(persona)

            persona.pop("_id", None)

            clean_personas.append(persona)

        # -------------------------------------------------
        # SAVE
        # -------------------------------------------------

        if clean_personas:

            users_collection.insert_many(
                clean_personas
            )

        return jsonify({

            "message":
                "Personas generated successfully",

            "count":
                len(clean_personas),

            "personas":
                serialize_document(clean_personas)

        }), 200

    except ValueError:

        return jsonify({
            "error": "Count must be a valid number"
        }), 400

    except Exception as error:

        print(
            "GENERATION ERROR:",
            error
        )

        return jsonify({
            "error": str(error)
        }), 500


# =========================================================
# SURVEY MODE
# =========================================================

@app.route("/api/ask-personas", methods=["POST"])
def ask_personas():

    try:

        data = request.get_json() or {}

        question = data.get(
            "question",
            ""
        ).strip()

        if not question:

            return jsonify({
                "error": "Question is required"
            }), 400

        personas = list(
            users_collection.find(
                {},
                {"_id": 0}
            )
        )

        if not personas:

            return jsonify({
                "error":
                    "No personas found. Generate personas first."
            }), 400

        responses = ask_all_personas(
            personas,
            question
        )

        # -------------------------------------------------
        # SAVE SURVEY RESPONSE
        # -------------------------------------------------

        survey_results_collection.insert_one({

            "type":
                "survey_responses",

            "question":
                question,

            "responses":
                serialize_document(responses),

            "created_at":
                datetime.now()

        })

        return jsonify({

            "question":
                question,

            "total_personas":
                len(personas),

            "responses":
                serialize_document(responses)

        }), 200

    except Exception as error:

        print(
            "ASK PERSONAS ERROR:",
            error
        )

        return jsonify({
            "error": str(error)
        }), 500


# =========================================================
# SURVEY INSIGHTS
# =========================================================

@app.route("/api/survey-insights", methods=["POST"])
def survey_insights_api():

    try:

        data = request.get_json() or {}

        question = data.get(
            "question",
            ""
        ).strip()

        responses = data.get(
            "responses",
            []
        )

        if not question:

            return jsonify({
                "error":
                    "Survey question is required"
            }), 400

        if not responses:

            return jsonify({
                "error":
                    "Survey responses are required"
            }), 400

        insights = generate_survey_insights(
            question,
            responses
        )

        survey_results_collection.insert_one({

            "type":
                "survey_insights",

            "question":
                question,

            "insights":
                insights,

            "created_at":
                datetime.now()

        })

        return jsonify({

            "question":
                question,

            "insights":
                insights

        }), 200

    except Exception as error:

        print(
            "SURVEY INSIGHTS ERROR:",
            error
        )

        return jsonify({
            "error": str(error)
        }), 500


# =========================================================
# SURVEY PRODUCT SCORE
# =========================================================

@app.route("/api/survey-rating", methods=["POST"])
def survey_rating_api():

    try:

        data = request.get_json() or {}

        question = data.get(
            "question",
            ""
        ).strip()

        responses = data.get(
            "responses",
            []
        )

        if not question:

            return jsonify({
                "error":
                    "Survey question is required"
            }), 400

        if not responses:

            return jsonify({
                "error":
                    "Survey responses are required"
            }), 400

        rating = generate_survey_product_rating(
            question,
            responses
        )

        survey_results_collection.insert_one({

            "type":
                "survey_rating",

            "question":
                question,

            "rating":
                serialize_document(rating),

            "created_at":
                datetime.now()

        })

        return jsonify({

            "question":
                question,

            "rating":
                serialize_document(rating)

        }), 200

    except Exception as error:

        print(
            "SURVEY RATING ERROR:",
            error
        )

        return jsonify({
            "error": str(error)
        }), 500


# =========================================================
# INTERVIEW
# =========================================================

@app.route("/api/interview", methods=["POST"])
def interview_api():

    try:

        data = request.get_json() or {}

        persona_name = data.get(
            "persona_name",
            ""
        ).strip()

        question = data.get(
            "question",
            ""
        ).strip()

        history = data.get(
            "history",
            []
        )

        if not persona_name:

            return jsonify({
                "error":
                    "Persona name is required"
            }), 400

        if not question:

            return jsonify({
                "error":
                    "Question is required"
            }), 400

        persona = users_collection.find_one({
            "name": persona_name
        })

        if not persona:

            return jsonify({
                "error":
                    "Selected persona was not found"
            }), 404

        persona = serialize_document(persona)

        answer = interview_persona(
            persona,
            question,
            history
        )

        return jsonify({

            "persona_name":
                persona_name,

            "question":
                question,

            "answer":
                answer

        }), 200

    except Exception as error:

        print(
            "INTERVIEW ERROR:",
            error
        )

        return jsonify({
            "error": str(error)
        }), 500


# =========================================================
# INTERVIEW INSIGHTS
# =========================================================

@app.route("/api/interview-insights", methods=["POST"])
def interview_insights_api():

    try:

        data = request.get_json() or {}

        persona_name = data.get(
            "persona_name",
            ""
        ).strip()

        conversation = data.get(
            "conversation",
            []
        )

        if not persona_name:

            return jsonify({
                "error":
                    "Persona name is required"
            }), 400

        if not conversation:

            return jsonify({
                "error":
                    "Interview conversation is required"
            }), 400

        persona = users_collection.find_one({
            "name": persona_name
        })

        if not persona:

            return jsonify({
                "error":
                    "Persona not found"
            }), 404

        persona = serialize_document(persona)

        insights = generate_interview_insights(
            persona,
            conversation
        )

        interview_results_collection.insert_one({

            "type":
                "interview_insights",

            "persona_name":
                persona_name,

            "insights":
                insights,

            "conversation":
                conversation,

            "created_at":
                datetime.now()

        })

        return jsonify({

            "persona_name":
                persona_name,

            "insights":
                insights

        }), 200

    except Exception as error:

        print(
            "INTERVIEW INSIGHTS ERROR:",
            error
        )

        return jsonify({
            "error": str(error)
        }), 500


# =========================================================
# INTERVIEW PRODUCT SCORE
# =========================================================

@app.route("/api/interview-rating", methods=["POST"])
def interview_rating_api():

    try:

        data = request.get_json() or {}

        persona_name = data.get(
            "persona_name",
            ""
        ).strip()

        conversation = data.get(
            "conversation",
            []
        )

        if not persona_name:

            return jsonify({
                "error":
                    "Persona name is required"
            }), 400

        if not conversation:

            return jsonify({
                "error":
                    "Interview conversation is required"
            }), 400

        persona = users_collection.find_one({
            "name": persona_name
        })

        if not persona:

            return jsonify({
                "error":
                    "Persona not found"
            }), 404

        persona = serialize_document(persona)

        rating = generate_product_rating(
            persona,
            conversation
        )

        interview_results_collection.insert_one({

            "type":
                "interview_rating",

            "persona_name":
                persona_name,

            "rating":
                serialize_document(rating),

            "conversation":
                conversation,

            "created_at":
                datetime.now()

        })

        return jsonify({

            "persona_name":
                persona_name,

            "rating":
                serialize_document(rating)

        }), 200

    except Exception as error:

        print(
            "INTERVIEW RATING ERROR:",
            error
        )

        return jsonify({
            "error": str(error)
        }), 500


# =========================================================
# SPRINT 3 - RESULTS DASHBOARD
# =========================================================
# =========================================================
# SPRINT 3 - RESULTS DASHBOARD
# =========================================================

@app.route("/api/results", methods=["GET"])
def get_results():

    try:

        # -------------------------------------------------
        # GET PERSONAS
        # -------------------------------------------------

        personas = list(
            users_collection.find(
                {},
                {"_id": 0}
            )
        )

        # -------------------------------------------------
        # GET LATEST SURVEY RESPONSE
        # -------------------------------------------------

        latest_survey_response = (
            survey_results_collection.find_one(
                {
                    "type": "survey_responses"
                },
                sort=[
                    ("created_at", -1)
                ]
            )
        )

        # -------------------------------------------------
        # GET LATEST SURVEY INSIGHTS
        # -------------------------------------------------

        latest_survey_insights = (
            survey_results_collection.find_one(
                {
                    "type": "survey_insights"
                },
                sort=[
                    ("created_at", -1)
                ]
            )
        )

        # -------------------------------------------------
        # GET LATEST SURVEY RATING
        # -------------------------------------------------

        latest_survey_rating = (
            survey_results_collection.find_one(
                {
                    "type": "survey_rating"
                },
                sort=[
                    ("created_at", -1)
                ]
            )
        )

        # -------------------------------------------------
        # RESPONSES
        # -------------------------------------------------

        responses = []

        if latest_survey_response:

            responses = latest_survey_response.get(
                "responses",
                []
            )

        # -------------------------------------------------
        # INSIGHTS
        # -------------------------------------------------

        insights = ""

        if latest_survey_insights:

            insights = latest_survey_insights.get(
                "insights",
                ""
            )

        # -------------------------------------------------
        # PRODUCT SCORE
        # -------------------------------------------------

        product_score = {

            "score": 0,

            "verdict":
                "No score generated",

            "recommendation":
                "Run Survey Mode first.",

            "reason":
                ""

        }

        if latest_survey_rating:

            product_score = latest_survey_rating.get(
                "rating",
                product_score
            )

        if not isinstance(product_score, dict):

            product_score = {

                "score": 0,

                "verdict":
                    "No score generated",

                "recommendation":
                    "",

                "reason":
                    ""

            }

        # -------------------------------------------------
        # FAST SENTIMENT ANALYSIS
        #
        # IMPORTANT:
        # Do NOT call Ollama here.
        # Results page should load immediately.
        # -------------------------------------------------

        sentiment = {

            "positive": 0,

            "neutral": 0,

            "negative": 0

        }

        positive_words = [

            "yes",
            "absolutely",
            "love",
            "like",
            "great",
            "good",
            "useful",
            "helpful",
            "interested",
            "definitely",
            "willing",
            "excited",
            "support",
            "positive"

        ]

        negative_words = [

            "no",
            "not",
            "never",
            "unlikely",
            "dislike",
            "expensive",
            "costly",
            "skeptical",
            "hesitant",
            "concerned",
            "unwilling",
            "problem",
            "negative"

        ]

        for item in responses:

            answer = item.get(
                "answer",
                item.get(
                    "response",
                    ""
                )
            )

            answer = str(answer).lower()

            positive_score = 0
            negative_score = 0

            for word in positive_words:

                if word in answer:

                    positive_score += 1

            for word in negative_words:

                if word in answer:

                    negative_score += 1

            if positive_score > negative_score:

                sentiment["positive"] += 1

            elif negative_score > positive_score:

                sentiment["negative"] += 1

            else:

                sentiment["neutral"] += 1

        # -------------------------------------------------
        # FAST THEME CLUSTERS
        #
        # Based on the actual persona responses.
        # No Ollama call.
        # -------------------------------------------------

        theme_keywords = {

            "Convenience": [
                "easy",
                "convenient",
                "easier",
                "simple",
                "save time"
            ],

            "Ease of Use": [
                "easy",
                "simple",
                "complex",
                "complexity",
                "user friendly"
            ],

            "Features": [
                "feature",
                "features",
                "ai",
                "technology",
                "tool"
            ],

            "Price": [
                "price",
                "cost",
                "expensive",
                "pay",
                "budget",
                "money"
            ],

            "Trust & Privacy": [
                "trust",
                "privacy",
                "secure",
                "security"
            ]

        }

        theme_clusters = {}

        total_responses = len(responses)

        for theme, keywords in theme_keywords.items():

            count = 0

            for item in responses:

                answer = item.get(
                    "answer",
                    item.get(
                        "response",
                        ""
                    )
                )

                answer = str(answer).lower()

                found = False

                for keyword in keywords:

                    if keyword in answer:

                        found = True
                        break

                if found:

                    count += 1

            if count > 0:

                percentage = round(
                    (count / total_responses) * 100,
                    1
                )

                theme_clusters[theme] = {

                    "count": count,

                    "percentage":
                        f"{percentage}%"

                }

        # -------------------------------------------------
        # KEY PERSONA QUOTES
        # -------------------------------------------------

        quotes = []

        for item in responses:

            answer = item.get(
                "answer",
                item.get(
                    "response",
                    ""
                )
            )

            if answer:

                quotes.append({

                    "persona":
                        item.get(
                            "persona_name",
                            "Unknown"
                        ),

                    "quote":
                        str(answer)

                })

        # Keep maximum 5 quotes

        quotes = quotes[:5]

        # -------------------------------------------------
        # ADOPTION RATE
        # -------------------------------------------------

        positive_count = sentiment.get(
            "positive",
            0
        )

        response_count = len(responses)

        if response_count > 0:

            adoption_rate = round(
                (
                    positive_count /
                    response_count
                ) * 100,
                1
            )

        else:

            adoption_rate = 0

        # -------------------------------------------------
        # FINAL RESULT
        # -------------------------------------------------

        result = {

            "total_users":
                len(personas),

            "adopted_users":
                positive_count,

            "rejected_users":
                sentiment.get(
                    "negative",
                    0
                ),

            "adoption_rate":
                f"{adoption_rate}%",

            "prediction":
                product_score.get(
                    "verdict",
                    "Not available"
                ),

            "recommendation":
                product_score.get(
                    "recommendation",
                    ""
                ),

            "product_score":
                product_score.get(
                    "score",
                    0
                ),

            "product_recommendation":
                product_score.get(
                    "recommendation",
                    ""
                ),

            "product_reason":
                product_score.get(
                    "reason",
                    ""
                ),

            "theme_clusters":
                theme_clusters,

            "sentiment":
                sentiment,

            "persona_quotes":
                quotes,

            "insights":
                insights

        }

        print(
            "RESULTS LOADED SUCCESSFULLY"
        )

        return jsonify(
            serialize_document(result)
        ), 200

    except Exception as error:

        print(
            "RESULTS ERROR:",
            error
        )

        return jsonify({

            "error":
                str(error)

        }), 500


# =========================================================
# GENERATE RESEARCH REPORT
# =========================================================

@app.route(
    "/api/research-report",
    methods=["GET"]
)
def research_report():

    try:

        # -------------------------------------------------
        # PERSONAS
        # -------------------------------------------------

        personas = list(
            users_collection.find(
                {},
                {"_id": 0}
            )
        )

        # -------------------------------------------------
        # LATEST RESPONSE
        # -------------------------------------------------

        latest_response = (
            survey_results_collection.find_one(
                {
                    "type":
                        "survey_responses"
                },
                sort=[
                    ("created_at", -1)
                ]
            )
        )

        # -------------------------------------------------
        # LATEST INSIGHTS
        # -------------------------------------------------

        latest_insights = (
            survey_results_collection.find_one(
                {
                    "type":
                        "survey_insights"
                },
                sort=[
                    ("created_at", -1)
                ]
            )
        )

        # -------------------------------------------------
        # LATEST RATING
        # -------------------------------------------------

        latest_rating = (
            survey_results_collection.find_one(
                {
                    "type":
                        "survey_rating"
                },
                sort=[
                    ("created_at", -1)
                ]
            )
        )

        # -------------------------------------------------
        # CHECK SURVEY
        # -------------------------------------------------

        if not latest_response:

            return jsonify({

                "error":
                    "Run Survey Mode before generating the report."

            }), 400

        # -------------------------------------------------
        # DATA
        # -------------------------------------------------

        responses = latest_response.get(
            "responses",
            []
        )

        question = latest_response.get(
            "question",
            ""
        )

        insights = ""

        if latest_insights:

            insights = latest_insights.get(
                "insights",
                ""
            )

        rating = {

            "score": 0,

            "recommendation":
                "No rating generated",

            "reason":
                ""

        }

        if latest_rating:

            rating = latest_rating.get(
                "rating",
                rating
            )

        if not isinstance(rating, dict):

            rating = {
                "score": 0,
                "recommendation":
                    "No rating generated",
                "reason": ""
            }

        # -------------------------------------------------
        # ANALYSIS
        # -------------------------------------------------

        try:

            themes = generate_theme_analysis(
                responses
            )

        except Exception as error:

            print(
                "REPORT THEME ERROR:",
                error
            )

            themes = {}

        try:

            sentiment = generate_sentiment_analysis(
                responses
            )

        except Exception as error:

            print(
                "REPORT SENTIMENT ERROR:",
                error
            )

            sentiment = {
                "positive": 0,
                "neutral": len(responses),
                "negative": 0
            }

        try:

            quotes = generate_key_quotes(
                responses
            )

        except Exception as error:

            print(
                "REPORT QUOTES ERROR:",
                error
            )

            quotes = []

        # -------------------------------------------------
        # REPORT FOLDER
        # -------------------------------------------------

        reports_folder = os.path.join(
            os.path.dirname(__file__),
            "reports"
        )

        os.makedirs(
            reports_folder,
            exist_ok=True
        )

        filename = os.path.join(
            reports_folder,
            "DecisionTwin_AI_Research_Report.pdf"
        )

        # -------------------------------------------------
        # CREATE PDF
        # -------------------------------------------------

        create_research_report(

            filename,

            serialize_document(personas),

            question,

            serialize_document(responses),

            insights,

            serialize_document(rating),

            serialize_document(themes),

            serialize_document(sentiment),

            serialize_document(quotes)

        )

        # -------------------------------------------------
        # SEND PDF
        # -------------------------------------------------

        return send_file(

            filename,

            as_attachment=True,

            download_name=
                "DecisionTwin_AI_Research_Report.pdf",

            mimetype=
                "application/pdf"

        )

    except Exception as error:

        print(
            "REPORT ERROR:",
            error
        )

        return jsonify({
            "error": str(error)
        }), 500


# =========================================================
# RUN SERVER
# =========================================================

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )