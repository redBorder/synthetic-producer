package net.redborder.utils.types;

import java.util.*;

public class RandomType implements Type {
    Map<String, String> typesName = new HashMap<>();
    Map<String, Type> types = new HashMap<>();
    List<String> uuids = new ArrayList<>();
    Random r = new Random();

    public RandomType(Map<String, Object> params) {
        Map<String, Map<String, Object>> components = (Map<String, Map<String, Object>>) params.get("components");

        for (Map.Entry<String, Map<String, Object>> component : components.entrySet()) {
            Type type = TypeManager.newType(component.getValue());
            String uuid = UUID.randomUUID().toString();
            uuids.add(uuid);
            typesName.put(uuid ,component.getKey());
            types.put(uuid, type);
        }
    }

    @Override
    public Object get() {
        String uuid = uuids.get(r.nextInt(uuids.size()));
        Type type = types.get(uuid);
        String typeName = typesName.get(uuid);

        Map<String, Object> typeValue = new HashMap<>();
        typeValue.put(typeName, type.get());

        return typeValue;
    }
}
