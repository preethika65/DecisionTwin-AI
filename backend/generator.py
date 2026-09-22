import ollama
import json
import re


# =========================================================
# MODEL CONFIGURATION
# =========================================================

MODEL = "qwen2.5:1.5b"


# =========================================================
# CLEAN JSON RESPONSE
# =========================================================

def clean_json_response(content):

    if not content:
        return ""

    content = content.strip()

    content = content.replace("```json", "")
    content = content.replace("```JSON", "")
    content = content.replace("```", "")

    return content.strip()


# =========================================================
# EXTRACT JSON OBJECT
# =========================================================

def extract_json_object(content):

    content = clean_json_response(content)

    match = re.search(
        r"\{.*\}",
        content,
        re.DOTALL
    )

    if match:
        return match.group()

    return content


# =========================================================
# EXTRACT JSON ARRAY
# =========================================================

def extract_json_array(content):

    content = clean_json_response(content)

    match = re.search(
        r"\[.*\]",
        content,
        re.DOTALL
    )

    if match:
        return match.group()

    return content


# =========================================================
# CALL OLLAMA
# =========================================================

def call_ollama(prompt, temperature=0.7):

    try:

        response = ollama.chat(
            model=MODEL,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            options={
                "temperature": temperature
            }
        )

        return response["message"]["content"].strip()

    except Exception as error:

        print(
            "\nOLLAMA ERROR:",
            error
        )

        return None


# =========================================================
# GENERATE SYNTHETIC PERSONAS
# =========================================================

def generate_personas(
    count,
    product,
    audience,
    research
):

    prompt = f"""
Generate exactly {count} realistic and meaningfully different
customer personas for product research.

PRODUCT:

{product}

TARGET AUDIENCE:

{audience}

RESEARCH OBJECTIVE:

{research}

These are realistic simulated customers.

Do NOT make everyone like the product.

Create a balanced mixture of:

- Strongly interested customer
- Interested but price-sensitive customer
- Practical customer
- Skeptical customer
- Privacy-conscious customer
- Customer worried about complexity
- Customer satisfied with existing alternatives
- Customer who does not need the product
- Customer who would use it only in certain situations

Each persona must be meaningfully different in:

- occupation
- income
- lifestyle
- priorities
- interests
- personality
- spending habits
- buying behavior

Do NOT make everyone:

- technology loving
- excited about innovation
- willing to pay
- likely to recommend the product

Some customers must naturally have neutral or negative opinions.

RETURN ONLY VALID JSON ARRAY.

Each persona must contain exactly:

name
age
gender
location
occupation
education
income
personality
interest
buying_behavior

Example:

[
    {{
        "name": "Emma",
        "age": 28,
        "gender": "Female",
        "location": "Hyderabad",
        "occupation": "Marketing Manager",
        "education": "Bachelor's Degree",
        "income": "₹8,00,000 per year",
        "personality": "Practical and cautious",
        "interest": "Cooking, travel, technology",
        "buying_behavior": "Compares alternatives carefully and buys only when value is clear"
    }}
]

Return exactly {count} personas.

Return JSON only.

Do not use markdown.

Do not include explanations.
"""

    try:

        content = call_ollama(
            prompt,
            temperature=0.9
        )

        if not content:
            return []

        print("\n========================================")
        print("OLLAMA PERSONA RESPONSE")
        print("========================================")
        print(content)
        print("========================================\n")

        content = extract_json_array(content)

        personas = json.loads(content)

        if not isinstance(personas, list):
            return []

        required_fields = [
            "name",
            "age",
            "gender",
            "location",
            "occupation",
            "education",
            "income",
            "personality",
            "interest",
            "buying_behavior"
        ]

        cleaned_personas = []

        for persona in personas:

            if not isinstance(persona, dict):
                continue

            cleaned_persona = {}

            for field in required_fields:

                cleaned_persona[field] = persona.get(
                    field,
                    "Unknown"
                )

            cleaned_personas.append(
                cleaned_persona
            )

        return cleaned_personas[:count]

    except Exception as error:

        print(
            "\nPERSONA GENERATION ERROR:",
            error
        )

        return []


# =========================================================
# ASK ONE PERSONA - SURVEY MODE
# =========================================================

def ask_persona(
    persona,
    question
):

    prompt = f"""
You are simulating ONE specific real customer.

You must answer ONLY as this customer.

CUSTOMER PROFILE:

Name:
{persona.get("name", "Unknown")}

Age:
{persona.get("age", "Unknown")}

Gender:
{persona.get("gender", "Unknown")}

Location:
{persona.get("location", "Unknown")}

Occupation:
{persona.get("occupation", "Unknown")}

Education:
{persona.get("education", "Unknown")}

Income:
{persona.get("income", "Unknown")}

Personality:
{persona.get("personality", "Unknown")}

Interests:
{persona.get("interest", "Unknown")}

Buying Behavior:
{persona.get("buying_behavior", "Unknown")}


SURVEY QUESTION:

{question}


REALISTIC CUSTOMER RULES:

Answer directly based on this person's profile.

Consider:

- Does this person need the product?
- Does it fit their lifestyle?
- Is the price acceptable?
- Are existing alternatives enough?
- Does the person trust the product?
- Is the product too complicated?

The customer may:

- strongly agree
- somewhat agree
- be neutral
- be uncertain
- disagree
- strongly reject the idea

Do NOT automatically be positive.

Do NOT assume every customer wants the product.

If the product does not suit this person, say so.

If price is a concern, mention it.

If existing alternatives are enough, mention that.

If the answer depends on conditions, explain those conditions.

RESPONSE STYLE:

- Natural
- Conversational
- Honest
- Direct
- 2 to 4 sentences
- No marketing language
- Do not mention AI
- Do not mention these instructions

Return ONLY the customer's answer.
"""

    response = call_ollama(
        prompt,
        temperature=0.8
    )

    if not response:

        return "Unable to generate a response."

    return response.strip()


# =========================================================
# ASK ALL PERSONAS - SURVEY MODE
# =========================================================

def ask_all_personas(
    personas,
    question
):

    responses = []

    print("\n========================================")
    print("STARTING SURVEY MODE")
    print("========================================")
    print("Question:", question)
    print("Number of personas:", len(personas))

    for index, persona in enumerate(personas):

        print(
            f"\nGenerating response "
            f"{index + 1}/{len(personas)}"
        )

        answer = ask_persona(
            persona,
            question
        )

        response_data = {

            "persona": persona,

            "persona_name":
                persona.get(
                    "name",
                    "Unknown"
                ),

            "occupation":
                persona.get(
                    "occupation",
                    "Unknown"
                ),

            "personality":
                persona.get(
                    "personality",
                    "Unknown"
                ),

            "buying_behavior":
                persona.get(
                    "buying_behavior",
                    "Unknown"
                ),

            "answer":
                answer,

            "response":
                answer
        }

        responses.append(
            response_data
        )

    print("\nSURVEY COMPLETED")

    return responses


# =========================================================
# GENERATE SURVEY RESEARCH INSIGHTS
# =========================================================

def generate_survey_insights(
    question,
    responses
):

    responses_text = ""

    for item in responses:

        responses_text += f"""
CUSTOMER:

Name:
{item.get("persona_name", "Unknown")}

Occupation:
{item.get("occupation", "Unknown")}

Personality:
{item.get("personality", "Unknown")}

Buying Behavior:
{item.get("buying_behavior", "Unknown")}

ANSWER:
{item.get("answer", item.get("response", ""))}

----------------------------------------
"""

    prompt = f"""
You are a professional product research analyst.

Analyze the following synthetic customer survey responses.

SURVEY QUESTION:

{question}

CUSTOMER RESPONSES:

{responses_text}

Create evidence-based research insights.

Use ONLY the actual responses.

Do not invent opinions.

Return ONLY valid JSON.

Use exactly this structure:

{{
    "overall_opinion": "Short summary of the overall customer opinion.",
    "positive_points": [
        "Positive point 1",
        "Positive point 2"
    ],
    "concerns": [
        "Concern 1",
        "Concern 2"
    ],
    "needs": [
        "Customer need 1",
        "Customer need 2"
    ],
    "pain_points": [
        "Pain point 1",
        "Pain point 2"
    ],
    "adoption_barriers": [
        "Adoption barrier 1",
        "Adoption barrier 2"
    ],
    "opportunities": [
        "Product opportunity 1",
        "Product opportunity 2"
    ],
    "conclusion": "Final research insight based only on the responses."
}}

Rules:

- Separate positive and negative opinions.
- Highlight disagreements.
- Mention uncertainty.
- Do not assume majority support.
- Do not invent information.
- Use only the customer responses.
- Keep each point concise.
- If a category is not clearly present, use an empty array.
- Return JSON only.
"""

    try:

        insights = call_ollama(
            prompt,
            temperature=0.2
        )

        if not insights:

            return {
                "overall_opinion":
                    "Unable to generate research insights.",
                "positive_points": [],
                "concerns": [],
                "needs": [],
                "pain_points": [],
                "adoption_barriers": [],
                "opportunities": [],
                "conclusion":
                    "The AI could not analyze the survey."
            }

        print("\n========================================")
        print("SURVEY RESEARCH INSIGHTS")
        print("========================================")
        print(insights)
        print("========================================\n")

        content = extract_json_object(
            insights
        )

        result = json.loads(content)

        return {
            "overall_opinion":
                result.get(
                    "overall_opinion",
                    ""
                ),

            "positive_points":
                result.get(
                    "positive_points",
                    []
                ),

            "concerns":
                result.get(
                    "concerns",
                    []
                ),

            "needs":
                result.get(
                    "needs",
                    []
                ),

            "pain_points":
                result.get(
                    "pain_points",
                    []
                ),

            "adoption_barriers":
                result.get(
                    "adoption_barriers",
                    []
                ),

            "opportunities":
                result.get(
                    "opportunities",
                    []
                ),

            "conclusion":
                result.get(
                    "conclusion",
                    ""
                )
        }

    except Exception as error:

        print(
            "\nSURVEY INSIGHTS ERROR:",
            error
        )

        return {
            "overall_opinion":
                "Unable to generate research insights.",

            "positive_points": [],

            "concerns": [],

            "needs": [],

            "pain_points": [],

            "adoption_barriers": [],

            "opportunities": [],

            "conclusion":
                "The AI could not analyze the survey."
        }


# =========================================================
# SURVEY PRODUCT RATING
# =========================================================

def generate_survey_product_rating(
    question,
    responses
):

    responses_text = ""

    for item in responses:

        responses_text += f"""
CUSTOMER:
{item.get("persona_name", "Unknown")}

OCCUPATION:
{item.get("occupation", "Unknown")}

PERSONALITY:
{item.get("personality", "Unknown")}

BUYING BEHAVIOR:
{item.get("buying_behavior", "Unknown")}

ANSWER:
{item.get("answer", item.get("response", ""))}

----------------------------------------
"""

    prompt = f"""
You are a professional product research analyst.

Calculate a realistic PRODUCT VALIDATION SCORE.

SURVEY QUESTION:

{question}

CUSTOMER RESPONSES:

{responses_text}

Consider:

- Positive opinions
- Negative opinions
- Neutral opinions
- Price concerns
- Adoption barriers
- Existing alternatives
- Customer uncertainty
- Overall willingness to use the product

Do NOT automatically give a high score.

If responses are mixed, use a middle score.

If many customers reject the product, reduce the score.

If customers strongly support it, increase the score.

Return ONLY valid JSON.

Use exactly:

{{
    "score": 75,
    "verdict": "Strong Potential",
    "recommendation": "Short practical recommendation.",
    "reason": "Short explanation based only on the survey responses."
}}

Score must be an integer between 0 and 100.

Return JSON only.
"""

    try:

        content = call_ollama(
            prompt,
            temperature=0.2
        )

        if not content:

            raise Exception(
                "No response from Ollama"
            )

        print(
            "\nSURVEY RATING RESPONSE:"
        )

        print(content)

        content = extract_json_object(
            content
        )

        rating = json.loads(content)

        score = int(
            float(
                rating.get(
                    "score",
                    50
                )
            )
        )

        score = max(
            0,
            min(100, score)
        )

        return {

            "score":
                score,

            "verdict":
                rating.get(
                    "verdict",
                    "Further validation required"
                ),

            "recommendation":
                rating.get(
                    "recommendation",
                    "Further validation is recommended."
                ),

            "reason":
                rating.get(
                    "reason",
                    ""
                )
        }

    except Exception as error:

        print(
            "\nSURVEY RATING ERROR:",
            error
        )

        return {

            "score": 0,

            "verdict":
                "Unable to calculate rating",

            "recommendation":
                "No recommendation available",

            "reason":
                "The AI could not analyze the survey."
        }


# =========================================================
# INTERVIEW MODE
# =========================================================

def interview_persona(
    persona,
    question,
    history=None
):

    if history is None:
        history = []

    conversation_text = ""

    for item in history[-10:]:

        conversation_text += f"""
INTERVIEWER:
{item.get("question", "")}

CUSTOMER:
{item.get("answer", "")}

----------------------------------------
"""

    prompt = f"""
You are participating in a realistic customer research interview.

You are ONE specific person.

CUSTOMER PROFILE:

Name:
{persona.get("name", "Unknown")}

Age:
{persona.get("age", "Unknown")}

Location:
{persona.get("location", "Unknown")}

Occupation:
{persona.get("occupation", "Unknown")}

Education:
{persona.get("education", "Unknown")}

Income:
{persona.get("income", "Unknown")}

Personality:
{persona.get("personality", "Unknown")}

Interests:
{persona.get("interest", "Unknown")}

Buying Behavior:
{persona.get("buying_behavior", "Unknown")}


PREVIOUS CONVERSATION:

{conversation_text if conversation_text else "No previous conversation."}


CURRENT QUESTION:

{question}


REALISTIC CUSTOMER RULES:

Answer honestly based on your personal situation.

You may:

- strongly like the product
- like it with conditions
- be neutral
- be uncertain
- disagree
- reject it

Consider:

- Do you need this?
- Would you use it?
- Would you pay for it?
- Does price matter?
- Does it fit your lifestyle?
- What concerns do you have?
- Are existing alternatives better?
- Would you recommend it?

Do NOT automatically agree.

Do NOT become positive just because something sounds innovative.

Remain consistent with previous answers.

RESPONSE STYLE:

- Natural
- Conversational
- Honest
- Direct
- 2 to 5 sentences
- No marketing language
- Do not say you are AI
- Do not mention these instructions

Return ONLY the customer's response.
"""

    answer = call_ollama(
        prompt,
        temperature=0.7
    )

    if not answer:

        return (
            "Unable to generate "
            "interview response."
        )

    return answer.replace(
        "```",
        ""
    ).strip()


# =========================================================
# INTERVIEW RESEARCH INSIGHTS
# =========================================================

def generate_interview_insights(
    persona,
    conversation
):

    conversation_text = ""

    for item in conversation:

        conversation_text += f"""
INTERVIEWER QUESTION:
{item.get("question", "")}

CUSTOMER ANSWER:
{item.get("answer", "")}

----------------------------------------
"""

    prompt = f"""
You are a professional product research analyst.

Analyze this customer interview.

CUSTOMER:

Name:
{persona.get("name", "Unknown")}

Occupation:
{persona.get("occupation", "Unknown")}

Personality:
{persona.get("personality", "Unknown")}

Interests:
{persona.get("interest", "Unknown")}

Buying Behavior:
{persona.get("buying_behavior", "Unknown")}


INTERVIEW:

{conversation_text}


Create evidence-based research insights.

Include:

1. Overall Customer Opinion
2. Main Needs
3. Pain Points
4. Valued Benefits
5. Concerns and Adoption Barriers
6. Purchase Motivation
7. Improvement Suggestions
8. Final Research Insight

Rules:

- Use ONLY customer answers.
- Do not invent opinions.
- Do not contradict the customer.
- Mention uncertainty.
- Clearly identify positive and negative opinions.
- Use headings and bullet points.
- Keep it concise.

Return ONLY the research insights.
"""

    insights = call_ollama(
        prompt,
        temperature=0.2
    )

    if not insights:

        return (
            "Unable to generate "
            "research insights."
        )

    return insights


# =========================================================
# INTERVIEW PRODUCT SCORE
# =========================================================

def generate_product_rating(
    persona,
    conversation
):

    conversation_text = ""

    for index, item in enumerate(
        conversation,
        start=1
    ):

        conversation_text += f"""
QUESTION {index}:

{item.get("question", "")}

CUSTOMER ANSWER:

{item.get("answer", "")}

----------------------------------------
"""

    prompt = f"""
You are a professional product research analyst.

Calculate a realistic PRODUCT RECOMMENDATION SCORE
for this specific customer.

CUSTOMER:

Name:
{persona.get("name", "Unknown")}

Occupation:
{persona.get("occupation", "Unknown")}

Personality:
{persona.get("personality", "Unknown")}

Buying Behavior:
{persona.get("buying_behavior", "Unknown")}


INTERVIEW:

{conversation_text}


Determine how likely this customer is to:

- Use the product
- Continue using it
- Recommend it

Base the score ONLY on the customer's answers.

Negative opinions reduce the score.

Concerns reduce the score.

Conditional opinions produce a middle score.

Uncertainty should not receive an extremely high score.

Return ONLY JSON.

Use exactly:

{{
    "score": 78,
    "recommendation": "Likely to use the product.",
    "reason": "Short reason based only on the interview."
}}

Score must be an integer from 0 to 100.
"""

    try:

        content = call_ollama(
            prompt,
            temperature=0.2
        )

        if not content:

            raise Exception(
                "No response from Ollama"
            )

        print(
            "\nINTERVIEW PRODUCT SCORE:"
        )

        print(content)

        content = extract_json_object(
            content
        )

        rating = json.loads(content)

        score = int(
            float(
                rating.get(
                    "score",
                    50
                )
            )
        )

        score = max(
            0,
            min(100, score)
        )

        return {

            "score":
                score,

            "recommendation":
                rating.get(
                    "recommendation",
                    "Further validation is recommended."
                ),

            "reason":
                rating.get(
                    "reason",
                    "The score is based on interview responses."
                )
        }

    except Exception as error:

        print(
            "\nINTERVIEW RATING ERROR:",
            error
        )

        return {

            "score": 0,

            "recommendation":
                "Unable to calculate recommendation score.",

            "reason":
                "The AI could not analyze the interview."
        }


# =========================================================
# SPRINT 3 - THEME ANALYSIS
# =========================================================

def generate_theme_analysis(
    responses
):

    text = ""

    for item in responses:

        text += (
            item.get(
                "answer",
                item.get(
                    "response",
                    ""
                )
            )
            + "\n"
        )

    prompt = f"""
Analyze the following customer responses.

RESPONSES:

{text}

Identify these five research themes:

1. Price
2. Features
3. Ease of Use
4. Trust & Privacy
5. Convenience

For each theme provide:

- count
- percentage
- short summary

Return ONLY valid JSON.

Use exactly:

{{
    "Price": {{
        "count": 2,
        "percentage": 40,
        "summary": "Customers discussed affordability."
    }},

    "Features": {{
        "count": 3,
        "percentage": 60,
        "summary": "Customers focused on useful features."
    }},

    "Ease of Use": {{
        "count": 2,
        "percentage": 40,
        "summary": "Some customers mentioned simplicity."
    }},

    "Trust & Privacy": {{
        "count": 1,
        "percentage": 20,
        "summary": "Privacy was mentioned by some customers."
    }},

    "Convenience": {{
        "count": 3,
        "percentage": 60,
        "summary": "Customers valued convenience."
    }}
}}
"""

    try:

        content = call_ollama(
            prompt,
            temperature=0.1
        )

        if not content:
            return {}

        content = extract_json_object(
            content
        )

        result = json.loads(content)

        return result

    except Exception as error:

        print(
            "THEME ANALYSIS ERROR:",
            error
        )

        return {}


# =========================================================
# SPRINT 3 - SENTIMENT ANALYSIS
# =========================================================

def generate_sentiment_analysis(
    responses
):

    text = ""

    for item in responses:

        text += (
            item.get(
                "answer",
                item.get(
                    "response",
                    ""
                )
            )
            + "\n"
        )

    prompt = f"""
Analyze the sentiment of these customer responses.

RESPONSES:

{text}

Classify responses as:

Positive
Neutral
Negative

Return ONLY JSON.

Use exactly:

{{
    "positive": 0,
    "neutral": 0,
    "negative": 0
}}

The three numbers must add up to the total number of responses.
"""

    try:

        content = call_ollama(
            prompt,
            temperature=0.1
        )

        if not content:

            return {
                "positive": 0,
                "neutral": 0,
                "negative": 0
            }

        content = extract_json_object(
            content
        )

        sentiment = json.loads(
            content
        )

        positive = int(
            sentiment.get(
                "positive",
                0
            )
        )

        neutral = int(
            sentiment.get(
                "neutral",
                0
            )
        )

        negative = int(
            sentiment.get(
                "negative",
                0
            )
        )

        total = len(responses)

        # Make sure counts stay valid.
        positive = max(
            0,
            positive
        )

        neutral = max(
            0,
            neutral
        )

        negative = max(
            0,
            negative
        )

        current_total = (
            positive
            + neutral
            + negative
        )

        # If Ollama gives invalid counts,
        # use a safe fallback.
        if current_total != total:

            print(
                "SENTIMENT COUNT MISMATCH"
            )

            positive = 0
            neutral = 0
            negative = 0

            for item in responses:

                answer = item.get(
                    "answer",
                    item.get(
                        "response",
                        ""
                    )
                ).lower()

                positive_words = [
                    "love",
                    "like",
                    "useful",
                    "great",
                    "good",
                    "helpful",
                    "definitely",
                    "worth",
                    "interested"
                ]

                negative_words = [
                    "hate",
                    "dislike",
                    "not interested",
                    "too expensive",
                    "too complicated",
                    "don't need",
                    "do not need",
                    "not useful",
                    "unlikely"
                ]

                has_positive = any(
                    word in answer
                    for word in positive_words
                )

                has_negative = any(
                    word in answer
                    for word in negative_words
                )

                if has_positive and not has_negative:

                    positive += 1

                elif has_negative and not has_positive:

                    negative += 1

                else:

                    neutral += 1

        return {

            "positive":
                positive,

            "neutral":
                neutral,

            "negative":
                negative
        }

    except Exception as error:

        print(
            "SENTIMENT ANALYSIS ERROR:",
            error
        )

        return {

            "positive": 0,

            "neutral": 0,

            "negative": 0
        }


# =========================================================
# SPRINT 3 - KEY QUOTES
# =========================================================

def generate_key_quotes(
    responses
):

    quotes = []

    for item in responses[:5]:

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
                        "Synthetic User"
                    ),

                "quote":
                    answer
            })

    return quotes