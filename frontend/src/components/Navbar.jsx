import { Link } from "react-router-dom";
import "../Styles/Navbar.css";


function Navbar(){

return(

<nav>

<h2>DecisionTwin AI</h2>


<div className="links">

<Link to="/">Home</Link>

<Link to="/dashboard">
Dashboard
</Link>

<Link to="/synthetic-users">
Synthetic Users
</Link>


<Link to="/scenario">
Scenario Creator
</Link>


<Link to="/simulation">
Simulation
</Link>


<Link to="/results">
Results
</Link>


</div>

</nav>

)

}

export default Navbar;