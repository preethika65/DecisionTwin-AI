import Idea from "../components/Idea";
import Features from "../components/Features";
import DashboardPreview from "../components/DashboardPreview";
import "../Styles/Home.css";

function Home() {

  return (
    <div className="app">

      <Idea />

      <Features />

      <DashboardPreview />

    </div>
  );
}

export default Home;