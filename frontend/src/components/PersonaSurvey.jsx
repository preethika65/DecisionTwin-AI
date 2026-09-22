import { useState } from "react";

function PersonaSurvey() {

  const [question, setQuestion] = useState("");
  const [responses, setResponses] = useState([]);
  const [insights, setInsights] = useState(null);
  const [rating, setRating] = useState(null);

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");


  // =====================================================
  // ASK ALL PERSONAS
  // =====================================================

  const askPersonas = async () => {

    if (!question.trim()) {

      setError("Please enter a question.");
      return;

    }


    setLoading(true);
    setError("");

    setResponses([]);
    setInsights(null);
    setRating(null);


    try {

      // =====================================================
      // STEP 1: ASK PERSONAS
      // =====================================================

      const response = await fetch(
        "http://localhost:5000/api/ask-personas",
        {

          method: "POST",

          headers: {
            "Content-Type": "application/json",
          },

          body: JSON.stringify({
            question: question.trim(),
          }),

        }
      );


      const data = await response.json();


      console.log(
        "SURVEY API RESPONSE:",
        data
      );


      if (!response.ok) {

        throw new Error(
          data.error ||
          "Unable to get persona responses."
        );

      }


      const personaResponses =
        data.responses || [];


      setResponses(personaResponses);


      // =====================================================
      // STEP 2: GENERATE SURVEY INSIGHTS
      // =====================================================

      if (personaResponses.length > 0) {

        console.log(
          "Generating survey research insights..."
        );


        const insightsResponse = await fetch(
          "http://localhost:5000/api/survey-insights",
          {

            method: "POST",

            headers: {
              "Content-Type": "application/json",
            },

            body: JSON.stringify({

              question: question.trim(),

              responses: personaResponses,

            }),

          }
        );


        const insightsData =
          await insightsResponse.json();


        console.log(
          "SURVEY INSIGHTS:",
          insightsData
        );


        if (insightsResponse.ok) {

          setInsights(
            insightsData.insights ||
            insightsData
          );

        }

      }


      // =====================================================
      // STEP 3: GENERATE PRODUCT RATING
      // =====================================================

      if (personaResponses.length > 0) {

        console.log(
          "Generating survey product rating..."
        );


        const ratingResponse = await fetch(
          "http://localhost:5000/api/survey-rating",
          {

            method: "POST",

            headers: {
              "Content-Type": "application/json",
            },

            body: JSON.stringify({

              question: question.trim(),

              responses: personaResponses,

            }),

          }
        );


        const ratingData =
          await ratingResponse.json();


        console.log(
          "SURVEY PRODUCT RATING:",
          ratingData
        );


        if (ratingResponse.ok) {

          setRating(
            ratingData.rating ||
            ratingData
          );

        }

      }


    } catch (error) {

      console.error(
        "Survey Error:",
        error
      );


      setError(
        error.message ||
        "Unable to complete survey analysis."
      );


    } finally {

      setLoading(false);

    }

  };


  return (

    <section className="persona-survey">


      {/* =====================================================
          HEADER
      ===================================================== */}

      <div className="survey-header">

        <h2>
          Ask Your Synthetic Users
        </h2>

        <p>
          Ask a question and see how your generated personas respond.
        </p>

      </div>


      {/* =====================================================
          QUESTION BOX
      ===================================================== */}

      <div className="survey-box">

        <textarea

          value={question}

          onChange={(e) => {

            setQuestion(e.target.value);

          }}

          placeholder="Example: Would you use this new AI feature?"

          rows={4}

          disabled={loading}

        />


        <button

          onClick={askPersonas}

          disabled={
            loading ||
            !question.trim()
          }

        >

          {loading
            ? "Analyzing Personas..."
            : "Ask Personas"}

        </button>

      </div>


      {/* =====================================================
          ERROR
      ===================================================== */}

      {error && (

        <div className="survey-error">

          {error}

        </div>

      )}


      {/* =====================================================
          LOADING
      ===================================================== */}

      {loading && (

        <div className="survey-loading">

          <p>
            🤖 AI is asking your synthetic users...
          </p>

          <p>
            🧠 Generating research insights and product score...
          </p>

        </div>

      )}


      {/* =====================================================
          RESPONSES
      ===================================================== */}

      {!loading &&
        responses.length > 0 && (

          <div className="responses">

            <h3>
              Persona Responses
            </h3>


            <div className="response-grid">


              {responses.map((item, index) => (

                <div
                  className="response-card"
                  key={index}
                >


                  {/* PERSONA NAME */}

                  <h4>

                    {item.persona_name ||
                      `Persona ${index + 1}`}

                  </h4>


                  {/* PERSONA INFORMATION */}

                  <div className="persona-info">


                    {item.occupation && (

                      <span>
                        💼 {item.occupation}
                      </span>

                    )}


                    {item.personality && (

                      <span>
                        🧠 {item.personality}
                      </span>

                    )}


                    {item.buying_behavior && (

                      <span>
                        🛒 {item.buying_behavior}
                      </span>

                    )}


                  </div>


                  {/* AI ANSWER */}

                  <div className="persona-answer">

                    <p>

                      {item.answer ||
                        item.response ||
                        "No response generated."}

                    </p>

                  </div>


                </div>

              ))}


            </div>


            {/* =====================================================
                SURVEY INSIGHTS
            ===================================================== */}

            {insights && (

              <div className="survey-insights">

                <h3>
                  🧠 AI Research Insights
                </h3>


                {typeof insights === "string" ? (

                  <p>{insights}</p>

                ) : (

                  <>

                    {insights.overall_opinion && (

                      <div>
                        <h4>Overall Opinion</h4>
                        <p>
                          {insights.overall_opinion}
                        </p>
                      </div>

                    )}


                    {insights.positive_points && (

                      <div>
                        <h4>Positive Points</h4>
                        <p>
                          {Array.isArray(
                            insights.positive_points
                          )
                            ? insights.positive_points.join(", ")
                            : insights.positive_points}
                        </p>
                      </div>

                    )}


                    {insights.concerns && (

                      <div>
                        <h4>Concerns</h4>
                        <p>
                          {Array.isArray(
                            insights.concerns
                          )
                            ? insights.concerns.join(", ")
                            : insights.concerns}
                        </p>
                      </div>

                    )}


                    {insights.needs && (

                      <div>
                        <h4>User Needs</h4>
                        <p>
                          {Array.isArray(
                            insights.needs
                          )
                            ? insights.needs.join(", ")
                            : insights.needs}
                        </p>
                      </div>

                    )}


                    {insights.conclusion && (

                      <div>
                        <h4>Conclusion</h4>
                        <p>
                          {insights.conclusion}
                        </p>
                      </div>

                    )}

                  </>

                )}

              </div>

            )}


            {/* =====================================================
                PRODUCT VALIDATION SCORE
            ===================================================== */}

            {rating && (

              <div className="survey-rating">

                <h3>
                  📊 Product Validation Score
                </h3>


                {rating.score !== undefined && (

                  <div className="rating-score">

                    {rating.score}/100

                  </div>

                )}


                {rating.recommendation && (

                  <p>

                    <b>
                      Recommendation:
                    </b>{" "}

                    {rating.recommendation}

                  </p>

                )}


                {rating.reason && (

                  <p>

                    <b>
                      Reason:
                    </b>{" "}

                    {rating.reason}

                  </p>

                )}

              </div>

            )}

          </div>

        )}


      {/* =====================================================
          NO RESPONSES
      ===================================================== */}

      {!loading &&
        !error &&
        responses.length === 0 && (

          <div className="no-responses">

            <p>
              Generate personas first, then ask them a question.
            </p>

          </div>

        )}


    </section>

  );

}


export default PersonaSurvey;