package net.redborder.utils.generators;

import net.redborder.utils.types.SetType;
import net.redborder.utils.types.Type;
import net.redborder.utils.types.TypeManager;

import java.util.HashMap;
import java.util.HashSet;
import java.util.Map;
import java.util.Set;

public class MessageGenerator implements Generator {
    private Map<String, Type> fields = new HashMap<>();
    private Set<String> sets = new HashSet<>();

    public MessageGenerator(Map<String, Object> fieldsDef) {
        for (Map.Entry<String, Object> entry : fieldsDef.entrySet()) {
            String fieldName = entry.getKey();
            Map<String, Object> params = (Map<String, Object>) entry.getValue();
            Type fieldType = TypeManager.newType(params);
            if(fieldType instanceof SetType) sets.add(fieldName);
            fields.put(fieldName, fieldType);
        }
        System.out.println("Sets: " + sets);
    }

    @Override
    public Map<String, Object> generate() {
        Map<String, Object> message = new HashMap<>();

        for (Map.Entry<String, Type> entry : fields.entrySet()) {
            String fieldName = entry.getKey();
            Object fieldValue = entry.getValue().get();

            if(!sets.contains(fieldName)) {
                message.put(fieldName, fieldValue);
            } else {
                message.putAll((Map<String, Object>) fieldValue);
            }
        }

        return message;
    }
}
