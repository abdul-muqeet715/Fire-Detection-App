import React, { useEffect, useState } from "react";
import  axios  from "axios";

import "../index.css";

const Table = () => {
  const [rowData, setRowData] = useState([]);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const allData = await axios.get("http://localhost:3001/getdata");
        console.log(allData);
        console.log("hello")
        for(var i in allData){
            console.log(i.data);
        }
        setRowData(allData.data);
      } catch (err) {
        console.error("Error is", err);
      }
    };
    fetchData();
  }, []);


  return (
    <div className="table">
      <table>
        <thead>
          <tr className="throw">
            {rowData.length > 0 &&
              Object.keys(rowData[0]).map((key) => <th key={key}>{key}</th>)}
          </tr>
        </thead>

        <tbody>
          {rowData.map((data, index) => (
            <tr className="tbrow" key={index}>
                {   Object.values(data).map(val=>(
                    <td key={val}>{val}</td>
                ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default Table;
