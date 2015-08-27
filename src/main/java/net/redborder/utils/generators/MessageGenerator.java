package net.redborder.utils.generators;

import net.redborder.utils.types.Type;
import net.redborder.utils.types.TypeManager;

import java.util.HashMap;
import java.util.Map;

public class MessageGenerator implements Generator {
    Map<String, Type> fields = new HashMap<>();

    public MessageGenerator(Map<String, Object> fieldsDef) {
        for (Map.Entry<String, Object> entry : fieldsDef.entrySet()) {
            String fieldName = entry.getKey();
            Map<String, Object> params = (Map<String, Object>) entry.getValue();
            Type fieldType = TypeManager.newType(params);
            fields.put(fieldName, fieldType);
        }
    }

    @Override
    public Map<String, Object> generate() {
        Map<String, Object> message = new HashMap<>();

        for (Map.Entry<String, Type> entry : fields.entrySet()) {
            String fieldName = entry.getKey();
            Object fieldValue = entry.getValue().get();
            message.put(fieldName, fieldValue);
        }

        return message;
    }
}
