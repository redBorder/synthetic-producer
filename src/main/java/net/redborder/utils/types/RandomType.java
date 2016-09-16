package net.redborder.utils.types;

import java.util.*;

public class RandomType implements Type {
    Map<String, String> typesName = new HashMap<>();
    Map<String, Type> types = new HashMap<>();
    List<String> uuids = new ArrayList<>();
    Random r = new Random();

    public RandomType(Map<String, Object> params) {
        List<Map<String, Map<String, Object>>> components = (List<Map<String, Map<String, Object>>>) params.get("components");

        for (Map<String, Map<String, Object>> component : components) {
            for(Map.Entry<String, Map<String, Object>> singleComponent : component.entrySet()) {
                Type type = TypeManager.newType(singleComponent.getValue());
                String uuid = UUID.randomUUID().toString();
                uuids.add(uuid);
                typesName.put(uuid, singleComponent.getKey());
                types.put(uuid, type);
            }
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
