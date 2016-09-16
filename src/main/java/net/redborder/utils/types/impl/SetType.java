package net.redborder.utils.types.impl;

import net.redborder.utils.types.MappedType;
import net.redborder.utils.types.Type;
import net.redborder.utils.types.TypeManager;

import java.util.*;

public class SetType extends MappedType {

    private List<Map<String, Object>> sets = new ArrayList<>();
    private Integer numbers = 0;
    private Random randomGen = new Random();

    private Map<String, Set<Object>> used = new HashMap<>();

    public SetType(Map<String, Object> params) {
        Map<String, Map<String, Object>> components = (Map<String, Map<String, Object>>) params.get("components");
        numbers = (Integer) params.get("numbers");

        Map<String, Type> componentsTypes = new HashMap<>();
        for (Map.Entry<String, Map<String, Object>> component : components.entrySet()) {
            componentsTypes.put(component.getKey(), TypeManager.newType(component.getValue()));
        }

        for (int i = 0; i < numbers; i++) {
            Map<String, Object> set = new HashMap<>();

            for (Map.Entry<String, Type> entryType : componentsTypes.entrySet()) {
                String name = entryType.getKey();
                Object value = entryType.getValue().get();

                Set<Object> usedSet = used.get(name);

                if (usedSet == null) {
                    Set<Object> newSet = new HashSet<>();
                    newSet.add(value);
                    used.put(name, newSet);
                } else {
                    Integer count = 0;
                    while (usedSet.contains(value) && count <= numbers) {
                        value = entryType.getValue().get();
                        count++;
                    }

                    usedSet.add(value);

                    used.put(name, usedSet);
                }

                if (entryType.getValue() instanceof MappedType) {
                    set.putAll((Map<String, Object>) value);
                } else {
                    set.put(name, value);
                }
            }

            sets.add(set);
        }

    }

    @Override
    public Map<String, Object> getMap() {
        return sets.get(randomGen.nextInt(numbers));
    }
}
