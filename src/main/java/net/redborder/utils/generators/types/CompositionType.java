package net.redborder.utils.generators.types;

import com.google.common.base.Joiner;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;

public class CompositionType implements Type {
    private String separator;
    private List<Type> components = new ArrayList<>();

    public CompositionType(Map<String, Object> params) {
        this.separator = (String) params.get("separator");
        List<Map<String, Object>> componentsList = (List<Map<String, Object>>) params.get("components");

        for (Map<String, Object> componentMap : componentsList) {
            Type componentType = TypeManager.newType(componentMap);
            components.add(componentType);
        }
    }

    @Override
    public Object get() {
        List<String> componentsResults = new ArrayList<>();

        for (Type type : components) {
            componentsResults.add(String.valueOf(type.get()));
        }

        return Joiner.on(separator).join(componentsResults);
    }
}
