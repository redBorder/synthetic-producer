package net.redborder.utils.generators;

import net.redborder.utils.types.*;

import java.util.HashMap;
import java.util.HashSet;
import java.util.Map;
import java.util.List;
import java.util.ArrayList;
import java.util.Set;

public class MessageGenerator implements Generator {
    private Map<String, Type> fields = new HashMap<>();
    private Set<String> mapComponents = new HashSet<>();
    private Integer nbrOfQuestions = 1;

    public MessageGenerator(Map<String, Object> fieldsDef) {
        for (Map.Entry<String, Object> entry : fieldsDef.entrySet()) {
            String fieldName = entry.getKey();
            Map<String, Object> params = (Map<String, Object>) entry.getValue();
            Type fieldType = TypeManager.newType(params);
            if(fieldType instanceof MappedType) mapComponents.add(fieldName);
            fields.put(fieldName, fieldType);
            if (fieldName.equals("questionnaire")) {
                Map<String, Object> questions = (Map<String, Object>) entry.getValue();
                this.nbrOfQuestions = ((List<String>) questions.get("questions")).size();
                System.out.println("nbr of questions : " + nbrOfQuestions);
            }
        }
        System.out.println("MapComponents: " + mapComponents);
    }

    @Override
    public  List<Map<String, Object>> generate() {
        List<Map<String, Object>> messageList = new ArrayList<>();
         for (int i = 0; i < nbrOfQuestions; i++) {
            Map<String, Object> message = new HashMap<>();
            for (Map.Entry<String, Type> entry : fields.entrySet()) {
                String fieldName = entry.getKey();
                Object fieldValue = entry.getValue().get();

                if(!mapComponents.contains(fieldName)) {
                    if (fieldName.equals("questionnaire"))
                      message.putAll((Map<String, Object>) fieldValue);
                    else 
                        message.put(fieldName, fieldValue);
                } else {
                    message.putAll((Map<String, Object>) fieldValue);
                }
            }
            messageList.add(message);
         }

        return messageList;
    }
}
