package com.fireDetection.fireApp.Entity;

import jakarta.persistence.*;
import lombok.Data;
import lombok.Getter;
import lombok.Setter;

import java.util.Date;

@Entity
@Data
@Getter
@Setter
@Table(name = "fire_incidents")
public class Fire {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)

    int id;
    String location;
    Date startTime;
    Date endTime;
    int duration;
    String mobileNumber;
    @Column(name="latitude")
    String latitude;
    @Column(name="longitude")
    String longitude;
    String videoUrl;

    public String getVideoUrl(){
        return this.videoUrl;
    }

}
