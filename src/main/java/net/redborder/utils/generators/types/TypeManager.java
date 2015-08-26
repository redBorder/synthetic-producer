package net.redborder.utils.generators.types;

import org.slf4j.Logger;
import java.lang.reflect.Constructor;
import java.lang.reflect.InvocationTargetException;
import java.util.HashMap;
import java.util.Map;

public class TypeManager {
    private final static Logger log = org.slf4j.LoggerFactory.getLogger(TypeManager.class);

    private static Map<String, Class> types = new HashMap<>();

    // Creates a new type with the parameters specified
    public static Type newType(Map<String, Object> params) {
        String typeName = (String) params.remove("type");
        Class typeClass = types.get(typeName);

        // The fallback type in case of error
        Type type = new ConstantType("type-" + typeName + "-not-found");

        // If this type wasn't used yet, get it from its name
        if (typeClass == null) {
            String capitalized = typeName.substring(0, 1).toUpperCase() + typeName.substring(1);
            String fullClassName = "net.redborder.utils.generators.types." + capitalized + "Type";

            try {
                typeClass = Class.forName(fullClassName);
                types.put(typeName, typeClass);
            } catch (ClassNotFoundException e) {
                log.error("Couldn't find the class associated with the type {}", typeName);
                typeClass = ConstantType.class;
            }
        }

        // Call the constructor with the parameters
        try {
            Constructor<Type> constructor = typeClass.getDeclaredConstructor(Map.class);
            type = constructor.newInstance(params);
        } catch (NoSuchMethodException | InstantiationException | InvocationTargetException | IllegalAccessException e) {
            log.error("Couldn't create the instance associated with the type {}", typeName, e);
        }

        return type;
    }
}
