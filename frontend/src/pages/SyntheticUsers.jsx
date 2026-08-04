import { useEffect, useState } from "react";
fetch("http://127.0.0.1:5000/api/users")
import "../Styles/SyntheticUsers.css";

function SyntheticUsers() {

  const [users, setUsers] = useState([]);

  useEffect(() => {
    fetch("http://127.0.0.1:5000/api/users")
      .then(response => response.json())
      .then(data => {
        setUsers(data);
      })
      .catch(error => {
        console.log("Error:", error);
      });
  }, []);


  return (
    <div className="synthetic-page">

      <h1>Synthetic Users</h1>

      <p className="subtitle">
        AI generated user profiles for decision simulation
      </p>

      <div className="user-grid">

        {users.map(user => (
          <div className="user-card" key={user.id}>

            <h2>{user.name}</h2>

            <p>
              <b>Age:</b> {user.age}
            </p>

            <p>
              <b>Location:</b> {user.location}
            </p>

            <p>
              <b>Behavior:</b> {user.behavior}
            </p>

          </div>
        ))}

      </div>

    </div>
  );
}

export default SyntheticUsers;