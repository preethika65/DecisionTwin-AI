import { useEffect, useState } from "react";
import API from "../api/api";
import "../Styles/Dashboard.css";

function Dashboard() {

  const [dashboard, setDashboard] = useState({
    users: 500,
    simulations: 25,
    accuracy: "94%"
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

    </div>
  );
}

export default Dashboard;