import { Link } from "react-router-dom";
import "../Styles/Home.css";

function Home() {

  return (

    <div className="home-page">

      {/* HERO */}

      <section className="home-hero">

        <div className="hero-badge">
          AI-POWERED CUSTOMER RESEARCH
        </div>

        <h1>
          Simulate Decisions.
          <br />

          <span>
            Predict Outcomes.
          </span>
        </h1>

        <p>
          DecisionTwin AI creates realistic synthetic users,
          simulates customer decisions, and transforms their
          responses into actionable product insights.
        </p>

        <div className="hero-buttons">

          <Link
            to="/synthetic-users"
            className="home-primary"
          >
            Create Synthetic Users →
          </Link>

          <Link
            to="/dashboard"
            className="home-secondary"
          >
            Explore Dashboard
          </Link>

        </div>

      </section>


      {/* STATS */}

      <section className="home-stats">

        <div>

          <strong>
            AI
          </strong>

          <span>
            Synthetic User Generation
          </span>

        </div>


        <div>

          <strong>
            100+
          </strong>

          <span>
            Customer Personas
          </span>

        </div>


        <div>

          <strong>
            2
          </strong>

          <span>
            Research Simulation Modes
          </span>

        </div>


        <div>

          <strong>
            100
          </strong>

          <span>
            Product Validation Score
          </span>

        </div>

      </section>


      {/* HOW IT WORKS */}

      <section className="how-section">

        <div className="section-heading">

          <span>
            HOW IT WORKS
          </span>

          <h2>
            From idea to research insight
          </h2>

          <p>
            Test your product concept with simulated
            customers before making real-world decisions.
          </p>

        </div>


        <div className="steps-grid">

          <div className="step-card">

            <div className="step-number">
              01
            </div>

            <div className="step-icon">
              👥
            </div>

            <h3>
              Generate Personas
            </h3>

            <p>
              Create diverse synthetic customers
              with realistic demographics,
              personalities and buying behavior.
            </p>

          </div>


          <div className="step-card">

            <div className="step-number">
              02
            </div>

            <div className="step-icon">
              💬
            </div>

            <h3>
              Ask Customers
            </h3>

            <p>
              Use Survey Mode or Interview Mode
              to understand how different
              customers respond.
            </p>

          </div>


          <div className="step-card">

            <div className="step-number">
              03
            </div>

            <div className="step-icon">
              🧠
            </div>

            <h3>
              Analyze Results
            </h3>

            <p>
              AI identifies themes, sentiment,
              customer needs, concerns and
              important opinions.
            </p>

          </div>


          <div className="step-card">

            <div className="step-number">
              04
            </div>

            <div className="step-icon">
              📊
            </div>

            <h3>
              Make Better Decisions
            </h3>

            <p>
              View the product validation score
              and generate a structured research
              report.
            </p>

          </div>

        </div>

      </section>


      {/* MODES */}

      <section className="modes-section">

        <div className="section-heading">

          <span>
            RESEARCH MODES
          </span>

          <h2>
            Understand customers from different angles
          </h2>

        </div>


        <div className="modes-grid">

          <Link
            to="/survey"
            className="mode-card"
          >

            <div>
              📋
            </div>

            <h3>
              Survey Mode
            </h3>

            <p>
              Ask one question to all synthetic
              users and compare their responses.
            </p>

            <span>
              Start Survey →
            </span>

          </Link>


          <Link
            to="/interview"
            className="mode-card"
          >

            <div>
              🎤
            </div>

            <h3>
              Interview Mode
            </h3>

            <p>
              Have a multi-turn conversation
              with an individual synthetic customer.
            </p>

            <span>
              Start Interview →
            </span>

          </Link>


          <Link
            to="/results"
            className="mode-card"
          >

            <div>
              📊
            </div>

            <h3>
              Results Dashboard
            </h3>

            <p>
              See themes, sentiment, quotes,
              insights and product validation.
            </p>

            <span>
              View Results →
            </span>

          </Link>

        </div>

      </section>


      {/* CTA */}

      <section className="home-cta">

        <h2>
          Ready to simulate your next decision?
        </h2>

        <p>
          Build your first synthetic customer
          research experiment with DecisionTwin AI.
        </p>

        <Link
          to="/synthetic-users"
          className="home-primary"
        >
          Start Building →
        </Link>

      </section>


      {/* FOOTER */}

      <footer className="home-footer">

        <strong>
          DecisionTwin AI
        </strong>

        <span>
          Simulate Decisions. Predict Outcomes.
          Build Better Futures.
        </span>

      </footer>

    </div>
  );
}

export default Home;