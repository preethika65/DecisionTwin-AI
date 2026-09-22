import { useEffect, useState } from "react";
import "../Styles/Results.css";

function Results() {

  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(true);
  const [reportLoading, setReportLoading] = useState(false);
  const [error, setError] = useState("");

  // =========================================================
  // LOAD RESULTS
  // =========================================================

  useEffect(() => {

    const getResults = async () => {

      try {

        const response = await fetch(
          "http://127.0.0.1:5000/api/results"
        );

        const data = await response.json();

        console.log("RESULTS DATA:", data);

        if (!response.ok) {

          throw new Error(
            data.error || "Unable to load results."
          );

        }

        setResult(data);

      } catch (error) {

        console.error(
          "RESULTS ERROR:",
          error
        );

        setError(error.message);

      } finally {

        setLoading(false);

      }

    };

    getResults();

  }, []);


  // =========================================================
  // DOWNLOAD RESEARCH REPORT
  // =========================================================

  const downloadReport = async () => {

    setReportLoading(true);
    setError("");

    try {

      const response = await fetch(
        "http://127.0.0.1:5000/api/research-report"
      );

      if (!response.ok) {

        let message = "Unable to generate report.";

        try {

          const data = await response.json();

          message =
            data.error || message;

        } catch {

          // Keep default message

        }

        throw new Error(message);

      }

      const blob =
        await response.blob();

      const url =
        window.URL.createObjectURL(blob);

      const link =
        document.createElement("a");

      link.href = url;

      link.download =
        "DecisionTwin_AI_Research_Report.pdf";

      document.body.appendChild(link);

      link.click();

      link.remove();

      window.URL.revokeObjectURL(url);

    } catch (error) {

      console.error(
        "REPORT ERROR:",
        error
      );

      setError(error.message);

    } finally {

      setReportLoading(false);

    }

  };


  // =========================================================
  // LOADING
  // =========================================================

  if (loading) {

    return (

      <div className="results-page">

        <div className="results-loading">

          <div className="loading-icon">
            📊
          </div>

          <h2>
            Loading Results...
          </h2>

          <p>
            DecisionTwin AI is loading
            your experiment results.
          </p>

        </div>

      </div>

    );

  }


  // =========================================================
  // ERROR
  // =========================================================

  if (error && !result) {

    return (

      <div className="results-page">

        <div className="error-box">
          ⚠️ {error}
        </div>

      </div>

    );

  }


  if (!result) {

    return (

      <div className="results-page">

        <div className="error-box">
          No results available yet.
        </div>

      </div>

    );

  }


  // =========================================================
  // SAFE DATA
  // =========================================================

  const themes =
    result.theme_clusters || {};

  const sentiment =
    result.sentiment || {};

  const quotes =
    result.persona_quotes || [];


  // =========================================================
  // PAGE
  // =========================================================

  return (

    <div className="results-page">


      {/* =================================================
          HEADER
      ================================================= */}

      <div className="results-header">

        <div>

          <span className="results-label">
            DECISIONTWIN AI
          </span>

          <h1>
            Insights & Experiment Results
          </h1>

          <p>
            Understand what your synthetic users
            are saying about the product.
          </p>

        </div>


        {/* PDF BUTTON */}

        <button
          className="report-button"
          onClick={downloadReport}
          disabled={reportLoading}
        >

          {reportLoading
            ? "Generating Report..."
            : "📄 Generate Research Report"
          }

        </button>

      </div>


      {/* =================================================
          ERROR MESSAGE
      ================================================= */}

      {error && (

        <div className="error-box">
          ⚠️ {error}
        </div>

      )}


      {/* =================================================
          PRODUCT VALIDATION
      ================================================= */}

      <section className="score-section">

        <div className="score-card">

          <div>

            <span className="card-label">
              PRODUCT VALIDATION
            </span>

            <h2>

              {result.product_score || 0}

              <span>
                /100
              </span>

            </h2>

            <p>

              {result.product_recommendation ||
                "No recommendation available."}

            </p>

          </div>


          <div className="score-circle">

            {result.product_score || 0}

          </div>

        </div>

      </section>


      {/* =================================================
          EXPERIMENT OVERVIEW
      ================================================= */}

      <section>

        <h2 className="section-title">
          Experiment Overview
        </h2>


        <div className="overview-grid">


          <div className="overview-card">

            <span>
              👥
            </span>

            <h3>
              {result.total_users || 0}
            </h3>

            <p>
              Synthetic Users
            </p>

          </div>


          <div className="overview-card">

            <span>
              👍
            </span>

            <h3>
              {result.adopted_users || 0}
            </h3>

            <p>
              Positive Responses
            </p>

          </div>


          <div className="overview-card">

            <span>
              👎
            </span>

            <h3>
              {result.rejected_users || 0}
            </h3>

            <p>
              Negative Responses
            </p>

          </div>


          <div className="overview-card">

            <span>
              📈
            </span>

            <h3>
              {result.adoption_rate || "0%"}
            </h3>

            <p>
              Positive Response Rate
            </p>

          </div>


        </div>

      </section>


      {/* =================================================
          THEME CLUSTERS
      ================================================= */}

      <section>

        <h2 className="section-title">
          Theme Clusters
        </h2>


        <div className="theme-grid">

          {Object.keys(themes).length > 0 ? (

            Object.entries(themes).map(
              ([theme, data]) => {

                const count =
                  typeof data === "object"
                    ? data.count || 0
                    : data || 0;

                const percentage =
                  typeof data === "object"
                    ? data.percentage || "0"
                    : "0";

                const summary =
                  typeof data === "object"
                    ? data.summary || ""
                    : "";

                return (

                  <div
                    className="theme-card"
                    key={theme}
                  >

                    <h3>
                      {theme}
                    </h3>

                    <div className="theme-number">
                      {count}
                    </div>

                    <p>

                      {percentage}

                      {String(percentage).includes("%")
                        ? ""
                        : "%"}

                      {" "}of responses

                    </p>


                    {summary && (

                      <small>
                        {summary}
                      </small>

                    )}

                  </div>

                );

              }
            )

          ) : (

            <div className="error-box">
              No theme data available.
            </div>

          )}

        </div>

      </section>


      {/* =================================================
          SENTIMENT BREAKDOWN
      ================================================= */}

      <section>

        <h2 className="section-title">
          Sentiment Breakdown
        </h2>


        <div className="sentiment-grid">


          <div className="sentiment-card positive">

            <span>
              😊
            </span>

            <h3>
              {sentiment.positive || 0}
            </h3>

            <p>
              Positive
            </p>

          </div>


          <div className="sentiment-card neutral">

            <span>
              😐
            </span>

            <h3>
              {sentiment.neutral || 0}
            </h3>

            <p>
              Neutral
            </p>

          </div>


          <div className="sentiment-card negative">

            <span>
              😟
            </span>

            <h3>
              {sentiment.negative || 0}
            </h3>

            <p>
              Negative
            </p>

          </div>


        </div>

      </section>


      {/* =================================================
          KEY PERSONA QUOTES
      ================================================= */}

      <section>

        <h2 className="section-title">
          Key Persona Quotes
        </h2>


        <div className="quotes-container">

          {quotes.length > 0 ? (

            quotes.map(
              (item, index) => (

                <div
                  className="quote-card"
                  key={index}
                >

                  <div className="quote-mark">
                    "
                  </div>

                  <p>

                    {item.quote ||
                      item.response ||
                      "No response available."}

                  </p>

                  <span>

                    —{" "}

                    {item.persona ||
                      item.persona_name ||
                      "Synthetic User"}

                  </span>

                </div>

              )
            )

          ) : (

            <div className="error-box">
              No persona quotes available.
            </div>

          )}

        </div>

      </section>


      {/* =================================================
          AI RESEARCH INSIGHTS
      ================================================= */}

      <section>

        <h2 className="section-title">
          AI Research Insights
        </h2>


        <div className="insights-card">


          <div className="insights-icon">
            🤖
          </div>


          <div>

            <h3>
              Research Analysis
            </h3>


            <div className="insights-text">

              {result.insights ? (

                typeof result.insights === "string" ? (

                  result.insights
                    .split("\n")
                    .map(
                      (line, index) => (

                        line.trim() && (

                          <p key={index}>
                            {line}
                          </p>

                        )

                      )
                    )

                ) : (

                  <div>

                    {result.insights.overall_opinion && (

                      <p>
                        <strong>
                          Overall Opinion:
                        </strong>{" "}
                        {result.insights.overall_opinion}
                      </p>

                    )}

                    {result.insights.positive_points && (

                      <p>
                        <strong>
                          Positive Points:
                        </strong>{" "}
                        {Array.isArray(
                          result.insights.positive_points
                        )
                          ? result.insights.positive_points.join(
                              " "
                            )
                          : result.insights.positive_points}
                      </p>

                    )}

                    {result.insights.concerns && (

                      <p>
                        <strong>
                          Concerns:
                        </strong>{" "}
                        {Array.isArray(
                          result.insights.concerns
                        )
                          ? result.insights.concerns.join(
                              " "
                            )
                          : result.insights.concerns}
                      </p>

                    )}

                    {result.insights.needs && (

                      <p>
                        <strong>
                          Needs:
                        </strong>{" "}
                        {Array.isArray(
                          result.insights.needs
                        )
                          ? result.insights.needs.join(
                              " "
                            )
                          : result.insights.needs}
                      </p>

                    )}

                    {result.insights.pain_points && (

                      <p>
                        <strong>
                          Pain Points:
                        </strong>{" "}
                        {Array.isArray(
                          result.insights.pain_points
                        )
                          ? result.insights.pain_points.join(
                              " "
                            )
                          : result.insights.pain_points}
                      </p>

                    )}

                    {result.insights.adoption_barriers && (

                      <p>
                        <strong>
                          Adoption Barriers:
                        </strong>{" "}
                        {Array.isArray(
                          result.insights.adoption_barriers
                        )
                          ? result.insights.adoption_barriers.join(
                              " "
                            )
                          : result.insights.adoption_barriers}
                      </p>

                    )}

                    {result.insights.opportunities && (

                      <p>
                        <strong>
                          Opportunities:
                        </strong>{" "}
                        {Array.isArray(
                          result.insights.opportunities
                        )
                          ? result.insights.opportunities.join(
                              " "
                            )
                          : result.insights.opportunities}
                      </p>

                    )}

                    {result.insights.conclusion && (

                      <p>
                        <strong>
                          Conclusion:
                        </strong>{" "}
                        {result.insights.conclusion}
                      </p>

                    )}

                  </div>

                )

              ) : (

                <p>
                  No research insights
                  generated yet.
                </p>

              )}

            </div>

          </div>

        </div>

      </section>


      {/* =================================================
          FINAL RECOMMENDATION
      ================================================= */}

      <section>

        <div className="final-card">

          <span className="card-label">
            AI DECISION SUMMARY
          </span>


          <h2>
            {result.prediction ||
              "Analysis Completed"}
          </h2>


          <p>
            {result.product_reason ||
              "No additional reasoning available."}
          </p>


          <div className="recommendation">

            {result.recommendation ||
              result.product_recommendation ||
              "No recommendation available."}

          </div>

        </div>

      </section>


      {/* =================================================
          RESEARCH REPORT
      ================================================= */}

      <section className="report-section">

        <h2>
          Research Report
        </h2>

        <p>
          Generate a structured PDF containing
          synthetic persona profiles, survey responses,
          theme clusters, sentiment analysis,
          key persona quotes, AI research insights
          and product validation results.
        </p>


        <button
          className="report-button large"
          onClick={downloadReport}
          disabled={reportLoading}
        >

          {reportLoading
            ? "Preparing PDF..."
            : "📄 Generate & Download PDF"
          }

        </button>

      </section>


    </div>

  );

}

export default Results;