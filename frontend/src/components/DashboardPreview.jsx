function DashboardPreview() {
  return (
    <section className="dashboard-preview">

      <h2>
        AI Simulation Dashboard
      </h2>

      <p className="dashboard-subtitle">
        Monitor simulations, user behavior, and AI predictions in real time.
      </p>


      <div className="dashboard-container">

        <div className="panel">

          <h3>Simulation Status</h3>

          <div className="status">
            <span className="dot"></span>
            AI Engine Running
          </div>

          <div className="metric">
            <h4>12,450</h4>
            <p>Active Synthetic Users</p>
          </div>

        </div>



        <div className="panel">

          <h3>Prediction Accuracy</h3>

          <div className="accuracy">
            94.8%
          </div>

          <p>
            Future outcome confidence
          </p>

        </div>



        <div className="panel chart">

          <h3>Decision Trends</h3>

          <div className="bars">
            <span></span>
            <span></span>
            <span></span>
            <span></span>
            <span></span>
          </div>

        </div>

      </div>

    </section>
  );
}

export default DashboardPreview;