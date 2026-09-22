import { BrowserRouter, Routes, Route } from "react-router-dom";

import Home from "./pages/Home";
import Dashboard from "./pages/Dashboard";
import SyntheticUsers from "./pages/SyntheticUsers";
import ScenarioCreator from "./pages/ScenarioCreator";
import Simulation from "./pages/Simulation";
import Results from "./pages/Results";
import Interview from "./pages/InterviewMode";
import PersonaSurvey from "./components/PersonaSurvey";


import Navbar from "./components/Navbar";

function App() {
  return (
    <BrowserRouter>

      <Navbar />

      <Routes>

        <Route path="/" element={<Home />} />

        <Route
          path="/dashboard"
          element={<Dashboard />}
        />

        <Route
          path="/synthetic-users"
          element={<SyntheticUsers />}
        />

        <Route
          path="/scenario"
          element={<ScenarioCreator />}
        />

        <Route
          path="/survey"
          element={<PersonaSurvey />}
        />

        <Route
          path="/interview"
          element={<Interview />}
        />

        <Route
          path="/simulation"
          element={<Simulation />}
        />

        <Route
          path="/results"
          element={<Results />}
        />
        

      </Routes>

    </BrowserRouter>
  );
}

export default App;