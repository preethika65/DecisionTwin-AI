import { useEffect, useState } from "react";
import "../Styles/SyntheticUsers.css";

function SyntheticUsers() {

  const [users, setUsers] = useState([]);


  useEffect(() => {

    const loadUsers = async () => {

      try {

        const response = await fetch(
          "http://127.0.0.1:5000/api/users"
        );

        const data = await response.json();

        console.log("USERS:", data);

        setUsers(data);

      } catch (error) {

        console.log("Error fetching users:", error);

      }

    };


    loadUsers();

  }, []);



  return (

    <div className="synthetic-page">

      <h1>Synthetic Users</h1>

      <p className="subtitle">
        AI-generated user profiles for decision simulation
      </p>


      <div className="user-grid">


        {
          users.map((user, index) => (

            <div className="user-card" key={index}>


              <h2>{user.name}</h2>


              <p>
                <b>Age:</b> {user.age}
              </p>


              <p>
                <b>Gender:</b> {user.gender}
              </p>


              <p>
                <b>Location:</b> {user.location}
              </p>


              <p>
                <b>Occupation:</b> {user.occupation}
              </p>


              <p>
                <b>Education:</b> {user.education}
              </p>


              <p>
                <b>Income:</b> {user.income}
              </p>


              <p>
                <b>Personality:</b> {user.personality}
              </p>


              <p>
                <b>Interests:</b>{" "}
                {
                  Array.isArray(user.interest)
                    ? user.interest.join(", ")
                    : user.interest || "Not available"
                }
              </p>


              <p>
                <b>Buying Behavior:</b>{" "}
                {
                  typeof user.buying_behavior === "object"
                    ? JSON.stringify(user.buying_behavior)
                    : user.buying_behavior || "Not available"
                }
              </p>


              {
                user.pain_points && (

                  <p>
                    <b>Pain Points:</b> {user.pain_points}
                  </p>

                )
              }


            </div>

          ))
        }


      </div>


    </div>

  );

}


export default SyntheticUsers;