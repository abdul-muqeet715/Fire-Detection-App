const express = require("express");
const { mongoose } = require("mongoose");
const FireIncident = require("./routes/FireIncidentRoute");
const app = express();

const cors = require("cors");

mongoose.connect('mongodb+srv://azimdamani:azimadamani.01@cluster0.0m5nzbt.mongodb.net/', { useNewUrlParser: true, useUnifiedTopology: true })
    .then(() => console.log("DB Connected"))
    .catch( err => console.error("Error", err));
app.use(cors());
app.use(express.json());

app.use("/", FireIncident);

app.listen(3001, ()=>{
    console.log("app started");
})