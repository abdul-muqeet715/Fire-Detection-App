package com.fireDetection.fireApp.Controller;

import com.fireDetection.fireApp.Entity.Fire;
import com.fireDetection.fireApp.Service.FireDetectionService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/")
public class FireAppController {

    @Autowired
    private FireDetectionService fireDetectionService;

    @CrossOrigin(origins = "http://localhost:4200")
    @GetMapping("/")
    public ResponseEntity<List<Fire>> getAllFireIncidents(){
        List<Fire> fireIncidents = fireDetectionService.getAllFireIncidents();
        return new ResponseEntity<>(fireIncidents, HttpStatus.OK);
    }

    @CrossOrigin(origins = "http://localhost:4200")
    @GetMapping("/video/{id}")
    public ResponseEntity<String> getUrlById(@PathVariable Long id) {
        String url = fireDetectionService.getVideoUrlByFireId(id);
        return new ResponseEntity<>(url,HttpStatus.OK);
    }
}
