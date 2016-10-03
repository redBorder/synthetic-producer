package net.redborder.utils.types.impl;

import net.redborder.utils.types.MappedType;
import net.redborder.utils.types.Type;
import net.redborder.utils.types.TypeManager;

import java.util.*;

public class SequentialType extends MappedType {

    List<Type> types = new LinkedList<>();
    List<String> fields = new LinkedList<>();
    Integer counter = 0;

    public SequentialType(Map<String, Object> params) {
        List<Map<String, Map<String, Object>>> components = (List<Map<String, Map<String, Object>>>) params.get("components");

        for (Map<String, Map<String, Object>> component : components) {
            for (Map.Entry<String, Map<String, Object>> singleComponent : component.entrySet()) {
                Type type = TypeManager.newType(singleComponent.getValue());
                types.add(type);
                fields.add(singleComponent.getKey());
            }
        }
    }

    @Override
    public Map<String, Object> getMap() {
        Type type = types.get(counter);

        Map<String, Object> typeValue = new HashMap<>();
        if (type instanceof MappedType) {
            typeValue.putAll((Map<String, Object>) type.get());
        } else {
            typeValue.put(fields.get(counter), type.get());
        }

        counter += 1;
        if(counter >= fields.size()) counter = 0;
        return typeValue;
    }
}
