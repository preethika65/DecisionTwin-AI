import { useEffect, useState } from "react";
import API from "../api/api";
import "../Styles/InterviewMode.css";

function Interview() {

  const [personas, setPersonas] = useState([]);
  const [selectedPersona, setSelectedPersona] = useState("");

  const [question, setQuestion] = useState("");
  const [messages, setMessages] = useState([]);

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  // =====================================================
  // RESEARCH INSIGHTS
  // =====================================================

  const [insights, setInsights] = useState("");
  const [insightsLoading, setInsightsLoading] = useState(false);


  // =====================================================
  // PRODUCT RATING
  // =====================================================

  const [rating, setRating] = useState(null);
  const [ratingLoading, setRatingLoading] = useState(false);


  // =====================================================
  // GET PERSONAS
  // =====================================================

  useEffect(() => {

    const getPersonas = async () => {

      try {

        const response = await API.get("/users");

        setPersonas(response.data);

      } catch (error) {

        console.error("PERSONA LOAD ERROR:", error);

        setError(
          "Unable to load personas. Generate personas first."
        );

      }

    };

    getPersonas();

  }, []);


  // =====================================================
  // ASK INTERVIEW QUESTION
  // =====================================================

  const askQuestion = async () => {

    if (!selectedPersona) {

      setError("Please select a persona.");
      return;

    }


    if (!question.trim()) {

      setError("Please enter a question.");
      return;

    }


    setLoading(true);
    setError("");


    try {

      // Create conversation history

      const history = messages.map((message) => ({

        question: message.question,

        answer: message.answer

      }));


      // Send interview request

      const response = await API.post(

        "/interview",

        {

          persona_name: selectedPersona,

          question: question.trim(),

          history: history

        }

      );


      // Add new question and answer

      setMessages((previousMessages) => [

        ...previousMessages,

        {

          question: question.trim(),

          answer: response.data.answer

        }

      ]);


      // Clear question input

      setQuestion("");


      // Clear old insights and rating
      // because conversation has changed

      setInsights("");

      setRating(null);


    } catch (error) {

      console.error("INTERVIEW ERROR:", error);

      setError(

        error.response?.data?.error ||

        "Unable to get interview response."

      );

    } finally {

      setLoading(false);

    }

  };


  // =====================================================
  // GET AI RESEARCH INSIGHTS
  // =====================================================

  const getResearchInsights = async () => {

    if (messages.length === 0) {

      setError(
        "Ask at least one interview question before generating insights."
      );

      return;

    }


    if (!selectedPersona) {

      setError("Please select a persona.");

      return;

    }


    setInsightsLoading(true);

    setError("");


    try {

      const response = await API.post(

        "/interview-insights",

        {

          persona_name: selectedPersona,

          conversation: messages

        }

      );


      // Save only insights

      setInsights(response.data.insights);


    } catch (error) {

      console.error("INSIGHTS ERROR:", error);

      setError(

        error.response?.data?.error ||

        "Unable to generate research insights."

      );

    } finally {

      setInsightsLoading(false);

    }

  };


  // =====================================================
  // GET PRODUCT RECOMMENDATION SCORE
  // =====================================================

  const getProductRating = async () => {

    if (messages.length === 0) {

      setError(
        "Ask interview questions before generating a product rating."
      );

      return;

    }


    if (!selectedPersona) {

      setError("Please select a persona.");

      return;

    }


    setRatingLoading(true);

    setError("");


    try {

      const response = await API.post(

        "/interview-rating",

        {

          persona_name: selectedPersona,

          conversation: messages

        }

      );


      console.log(
        "INTERVIEW RATING RESPONSE:",
        response.data
      );


      // =================================================
      // IMPORTANT FIX
      //
      // Backend response:
      //
      // {
      //   persona_name: "...",
      //   rating: {
      //      score: 78,
      //      recommendation: "...",
      //      reason: "..."
      //   }
      // }
      //
      // So save ONLY response.data.rating
      // =================================================

      setRating(response.data.rating);


    } catch (error) {

      console.error("RATING ERROR:", error);

      setError(

        error.response?.data?.error ||

        "Unable to generate product rating."

      );

    } finally {

      setRatingLoading(false);

    }

  };


  // =====================================================
  // CLEAR INTERVIEW
  // =====================================================

  const clearInterview = () => {

    setMessages([]);

    setQuestion("");

    setError("");

    setInsights("");

    setRating(null);

  };


  // =====================================================
  // RETURN UI
  // =====================================================

  return (

    <div className="interview-page">


      {/* =====================================================
          HEADER
      ===================================================== */}

      <div className="interview-header">

        <div>

          <h1>Interview Mode</h1>

          <p>
            Select a synthetic user and conduct a realistic
            AI-powered interview.
          </p>

        </div>


        <button
          className="clear-btn"
          onClick={clearInterview}
        >

          Clear Interview

        </button>

      </div>


      {/* =====================================================
          PERSONA SELECTION
      ===================================================== */}

      <div className="persona-selection">

        <h3>Select Synthetic User</h3>


        <select

          value={selectedPersona}

          onChange={(e) => {

            setSelectedPersona(e.target.value);

            setMessages([]);

            setInsights("");

            setRating(null);

            setError("");

          }}

        >

          <option value="">
            -- Select a Persona --
          </option>


          {personas.map((persona, index) => (

            <option
              key={index}
              value={persona.name}
            >

              {persona.name} — {persona.occupation}

            </option>

          ))}

        </select>


        {personas.length === 0 && (

          <p className="no-personas">

            No synthetic users found.
            Please generate personas first.

          </p>

        )}

      </div>


      {/* =====================================================
          INTERVIEW CHAT
      ===================================================== */}

      <div className="interview-chat">


        {messages.length === 0 ? (

          <div className="empty-chat">

            <div className="empty-icon">
              🎤
            </div>

            <h2>Start Your Interview</h2>

            <p>
              Select a synthetic user and ask your
              first question.
            </p>

          </div>

        ) : (

          messages.map((message, index) => (

            <div
              className="conversation"
              key={index}
            >


              {/* USER QUESTION */}

              <div className="question-message">

                <span className="message-label">
                  YOU
                </span>

                <p>
                  {message.question}
                </p>

              </div>


              {/* PERSONA ANSWER */}

              <div className="answer-message">

                <span className="message-label">
                  {selectedPersona}
                </span>

                <p>
                  {message.answer}
                </p>

              </div>

            </div>

          ))

        )}


        {loading && (

          <div className="thinking">

            🤖 {selectedPersona} is thinking...

          </div>

        )}

      </div>


      {/* =====================================================
          QUESTION INPUT
      ===================================================== */}

      <div className="question-box">

        <textarea

          value={question}

          onChange={(e) =>
            setQuestion(e.target.value)
          }

          placeholder={
            selectedPersona
              ? `Ask ${selectedPersona} a question...`
              : "Select a persona first..."
          }

          rows="3"

          disabled={!selectedPersona || loading}

        />


        <button

          className="ask-btn"

          onClick={askQuestion}

          disabled={
            !selectedPersona ||
            !question.trim() ||
            loading
          }

        >

          {loading
            ? "Thinking..."
            : "Ask Question"}

        </button>

      </div>


      {/* =====================================================
          AI ACTION BUTTONS
      ===================================================== */}

      <div className="interview-actions">


        {/* AI RESEARCH INSIGHTS */}

        <button

          className="insights-btn"

          onClick={getResearchInsights}

          disabled={
            messages.length === 0 ||
            insightsLoading
          }

        >

          {insightsLoading
            ? "Analyzing Interview..."
            : "🧠 AI Research Insights"}

        </button>


        {/* PRODUCT RECOMMENDATION SCORE */}

        <button

          className="rating-btn"

          onClick={getProductRating}

          disabled={
            messages.length === 0 ||
            ratingLoading
          }

        >

          {ratingLoading
            ? "Calculating Score..."
            : "⭐ Product Recommendation Score"}

        </button>


      </div>


      {/* =====================================================
          RESEARCH INSIGHTS RESULT
      ===================================================== */}

      {insights && (

        <div className="insights-box">

          <h2>
            🧠 AI Research Insights
          </h2>


          <div className="insights-content">

            {insights}

          </div>

        </div>

      )}


      {/* =====================================================
          PRODUCT RECOMMENDATION SCORE RESULT
      ===================================================== */}

      {rating && (

        <div className="rating-box">

          <h2>
            ⭐ Product Recommendation Score
          </h2>


          {/* NUMERIC SCORE */}

          <div className="rating-score">

            {rating.score ?? 0}/100

          </div>


          {/* RECOMMENDATION */}

          {rating.recommendation && (

            <div className="rating-label">

              {rating.recommendation}

            </div>

          )}


          {/* REASON */}

          {rating.reason && (

            <p className="rating-reason">

              {rating.reason}

            </p>

          )}

        </div>

      )}


      {/* =====================================================
          ERROR
      ===================================================== */}

      {error && (

        <div className="interview-error">

          {error}

        </div>

      )}


    </div>

  );

}

export default Interview;
