package net.redborder.utils.types.impl;

import net.redborder.utils.types.MappedType;
import net.redborder.utils.types.Type;
import net.redborder.utils.types.TypeManager;

import java.util.HashMap;
import java.util.Map;

public class HashmapType extends MappedType {
    Map<String, Type> types = new HashMap<>();

    public HashmapType(Map<String, Object> params) {
        Map<String, Map<String, Object>> components = (Map<String, Map<String, Object>>) params.get("components");

        for (Map.Entry<String, Map<String, Object>> component : components.entrySet()) {
            Type type = TypeManager.newType(component.getValue());
            types.put(component.getKey(), type);
        }
    }

    @Override
    public Map<String, Object> getMap() {
        Map<String, Object> map = new HashMap<>();
        for(Map.Entry<String, Type> type : types.entrySet()){
            if (type.getValue() instanceof MappedType) {
                map.putAll((Map<String, Object>) type.getValue().get());
            } else {
                map.put(type.getKey(), type.getValue().get());
            }
        }
        return map;
    }
}
