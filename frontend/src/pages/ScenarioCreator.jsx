import { useState } from "react";
import "../Styles/ScenarioCreator.css";

function ScenarioCreator() {

  const [scenario, setScenario] = useState({
    scenario_name: "",
    decision: "",
    target_users: ""
  });


  const handleChange = (e) => {

    setScenario({
      ...scenario,
      [e.target.name]: e.target.value
    });

  };


  const createScenario = () => {

    fetch("http://127.0.0.1:5000/api/scenario", {

      method: "POST",

      headers: {
        "Content-Type": "application/json"
      },

      body: JSON.stringify(scenario)

    })

    .then(response => response.json())

    .then(data => {

      alert(data.status);


      // clear form after creation
      setScenario({
        scenario_name: "",
        decision: "",
        target_users: ""
      });

    })

    .catch(error => {

      console.log("Error:", error);

      alert("Scenario creation failed");

    });

  };


  return (

    <div className="scenario-page">


      <h1>Scenario Creator</h1>


      <p>
        Create what-if scenarios for AI simulation.
      </p>



      <input

        name="scenario_name"

        placeholder="Scenario Name"

        value={scenario.scenario_name}

        onChange={handleChange}

      />



      <input

        name="decision"

        placeholder="Decision Change"

        value={scenario.decision}

        onChange={handleChange}

      />



      <input

        name="target_users"

        placeholder="Target Users"

        value={scenario.target_users}

        onChange={handleChange}

      />



      <button onClick={createScenario}>

        Create Scenario

      </button>



    </div>

  );

}


export default ScenarioCreator;