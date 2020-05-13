import React, { useState, useEffect } from "react";

export default function DataLoader() {
  const [data, setData] = useState([]);

 const update = () => {

    fetch("http://localhost:8081/v1/tasks/")
      .then(response => response.json())
      .then(data => setData(data))
      .catch(error => console.log(error));
  }

  return (
    <div>
      <button onClick={update}>fetch results</button>
  
      <li>
      {JSON.stringify(data)}
      </li>
    </div>
  );
}