package net.redborder.utils.types;

import java.util.*;

public class RandomType implements Type {
    List<Type> types = new ArrayList<>();
    Random r = new Random();

    public RandomType(Map<String, Object> params) {
        Map<String, Map<String, Object>> components = (Map<String, Map<String, Object>>) params.get("components");

        for (Map.Entry<String, Map<String, Object>> component : components.entrySet()) {
            types.add(TypeManager.newType(component.getValue()));
        }
    }

    @Override
    public Object get() {
        return types.get(r.nextInt(types.size())).get();
    }
}
