package net.redborder.utils.types.impl;

import net.redborder.utils.types.MappedType;

import java.util.HashMap;
import java.util.Map;
import java.util.Random;

public class CoordinatesType extends MappedType {
    private Random randomGen = new Random();
    private Double latPoint, longPoint;
    private Integer radius;
    private String latitudeDim, longitudeDim;
    private Integer truncate;

    public CoordinatesType(Map<String, Object> params) {
        this.latPoint = (Double) params.get("latPoint");
        this.longPoint = (Double) params.get("longPoint");
        this.radius = (Integer) params.get("radius");
        this.latitudeDim = (String) params.get("latitudeDim");
        this.longitudeDim = (String) params.get("longitudeDim");
        this.truncate = (Integer) params.get("truncate");
    }

    @Override
    public Map<String, Object> getMap() {
        Double rd = radius / 111300d;
        Double u = Math.random();
        Double v = Math.random();

        Double w = rd * Math.sqrt(u);
        Double t = 2 * Math.PI * v;
        Double x = w * Math.cos(t);
        Double y = w * Math.sin(t);

        Map<String, Object> coordinates = new HashMap<>();
        coordinates.put(latitudeDim, Math.floor((y + latPoint) * truncate) / truncate);
        coordinates.put(longitudeDim, Math.floor((x + longPoint) * truncate) / truncate);

        return coordinates;
    }
}
