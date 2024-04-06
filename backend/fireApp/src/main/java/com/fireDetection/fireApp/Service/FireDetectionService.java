package com.fireDetection.fireApp.Service;

import com.fireDetection.fireApp.Entity.Fire;
import com.fireDetection.fireApp.Repository.FireRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.Optional;

@Service
public class FireDetectionService {

    @Autowired
    FireRepository fireRepository;
    public List<Fire> getAllFireIncidents() {
        return (List<Fire>) fireRepository.findAll();
    }

    public String getVideoUrlByFireId(Long id) {
        Fire fire = fireRepository.findById(id).get();
        return fire.getVideoUrl();
    }
}
