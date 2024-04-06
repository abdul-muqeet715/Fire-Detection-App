package com.fireDetection.fireApp.Repository;

import com.fireDetection.fireApp.Entity.Fire;
import org.springframework.data.repository.CrudRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface FireRepository extends CrudRepository<Fire,Long> {
}
