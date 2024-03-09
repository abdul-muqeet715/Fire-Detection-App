const mongoose = require("mongoose");

const DataSchema = new mongoose.Schema({
    id: { type: String, require: true },
    IncidentLocation: { type: String, require: true },
    fireStationId: { type: String, required: true },
    fireStationLocation: { type: String, required: true },
    fireStationPhoneNumber: { type: String, required: true },
    date: { type: Date, default: Date.now },
    time: { type: String, required: true },
    videoFootage: { type: String, required: true }
});

const FireIncident = mongoose.model('FireIncident' , DataSchema);

module.exports = FireIncident;

