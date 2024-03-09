const express = require("express")
const router = express.Router();

const FireIncident = require("../model/Data");

router.get("/getdata" , async (req, res) =>{
    try{
        const alldata = await FireIncident.find();
        res.json(alldata);
    }
    catch(err){
        console.log(err);
        res.status(500).json({message : err.message});
    }


} );

router.post("/add" , async(req, res) =>{
    try{

        const newincident = await FireIncident.create(req.body);
        res.status(200).json(newincident);

    }
    catch(err){
        res.status(500).json({message: error.message})
    }
} );



module.exports = router;