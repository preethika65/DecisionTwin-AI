import { useEffect, useState } from "react";
import API from "../api/api";
import PersonaSurvey from "../components/PersonaSurvey";
import "../Styles/Dashboard.css";

function Dashboard() {

  const [dashboard, setDashboard] = useState({
    users: 0,
    simulations: 0,
    accuracy: "0%"
  });

  useEffect(() => {

    API.get("/dashboard")
      .then((response) => {
        setDashboard(response.data);
      })
      .catch((error) => {
        console.log("Dashboard API Error:", error);
      });

  }, []);

  return (
    <div className="dashboard">

      <h1>DecisionTwin AI Dashboard</h1>

      <div className="stats">

        <div className="card users">
          <h2>{dashboard.users}</h2>
          <p>Synthetic Users</p>
        </div>

        <div className="card simulations">
          <h2>{dashboard.simulations}</h2>
          <p>Simulations</p>
        </div>

        <div className="card accuracy">
          <h2>{dashboard.accuracy}</h2>
          <p>Accuracy</p>
        </div>

      </div>

      {/* Ask Synthetic Users */}

      <PersonaSurvey />

    </div>
  );
}

export default Dashboard;