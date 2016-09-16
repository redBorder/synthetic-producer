package net.redborder.utils.types;

import java.util.*;

public class RandomType implements Type {
    List<String> typesName = new ArrayList<>();
    Map<String, Type> types = new HashMap<>();
    Random r = new Random();

    public RandomType(Map<String, Object> params) {
        Map<String, Map<String, Object>> components = (Map<String, Map<String, Object>>) params.get("components");

        for (Map.Entry<String, Map<String, Object>> component : components.entrySet()) {
            Type type = TypeManager.newType(component.getValue());
            typesName.add(component.getKey());
            types.put(component.getKey(), type);
        }
    }

    @Override
    public Object get() {
        String typeName = typesName.get(r.nextInt(typesName.size()));
        Type type = types.get(typeName);

        Map<String, Object> typeValue = new HashMap<>();
        typeValue.put(typeName, type.get());

        return typeValue;
    }
}
