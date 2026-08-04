function Idea() {
  return (
    <section className="hero">

      <div className="hero-content">

        <h1>
          Simulate Decisions.
          <br />
          Predict Outcomes.
          <br />
          Build Better Futures.
        </h1>

        <p>
          An AI-powered digital twin platform that creates synthetic users,
          runs scenarios, and generates actionable insights.
        </p>

        <div className="hero-buttons">

          <button className="primary-btn">
            Create Simulation
          </button>

          <button className="secondary-btn">
            Explore Dashboard
          </button>

        </div>

      </div>


      <div className="hero-dashboard">

        <div className="dashboard-card">

          <h3>
            AI Simulation Dashboard
          </h3>

          <div className="stats">

            <div>
              <span>10K+</span>
              <small>Synthetic Users</small>
            </div>

            <div>
              <span>95%</span>
              <small>Prediction Accuracy</small>
            </div>

          </div>

          <div className="graph">
            Decision Analysis ↑
          </div>

        </div>

      </div>

    </section>
  );
}

export default Idea;
