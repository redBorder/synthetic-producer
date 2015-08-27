package net.redborder.utils.types;

import java.util.List;
import java.util.Map;
import java.util.Random;

public class CollectionType implements Type {
    private Random randomGen = new Random();
    private List<String> values;

    public CollectionType(Map<String, Object> params) {
        this.values = (List<String>) params.get("values");
    }

    @Override
    public Object get() {
        int random = randomGen.nextInt(Integer.MAX_VALUE);
        int randomIndex = random % values.size();
        return values.get(randomIndex);
    }
}
