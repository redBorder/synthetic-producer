package net.redborder.utils;

import org.ho.yaml.Yaml;
import org.ho.yaml.exception.YamlException;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.io.File;
import java.io.FileNotFoundException;
import java.util.Collections;
import java.util.Map;
import java.util.Set;

public class ConfigFile {
    private static final Logger log = LoggerFactory.getLogger(ConfigFile.class);
    private String configFile;
    private Map<String, Object> map;

    public ConfigFile(String configFile) {
        this.configFile = configFile;

        if (this.configFile == null) {
            this.configFile = "./config.yml";
        }

        reload();
    }

    public void reload() {
        try {
            map = (Map<String, Object>) Yaml.load(new File(configFile));
        } catch (FileNotFoundException e) {
            log.error("Couldn't find config file {}", configFile);
            System.exit(1);
        } catch (YamlException e) {
            log.error("Couldn't read config file {}. Is it a YAML file?", configFile);
            System.exit(1);
        }
    }

    /**
     * Getter.
     *
     * @param property Property to read from the general section
     * @return Property read
     */

    public <T> T get(String property) {
        T ret = null;

        if (map != null) {
            ret = (T) map.get(property);
        }

        return ret;
    }

    /**
     * Getter with a default value
     *
     * @param property Property to read from the general section
     *                 If it's not present on the section, give it a default value
     * @return Property read
     */

    public <T> T getOrDefault(String property, T defaultValue) {
        T fromFile = get(property);
        T ret = (fromFile == null ? defaultValue : fromFile);
        return ret;
    }

    /**
     * Gets the list of keys from a map.
     *
     * @param property Property to read from the general section
     * @return Property read
     */
    public Set<String> getKeys(String property) {
        Map<String, Object> fromFile = get(property);
        Set<String> emptySet = Collections.emptySet();
        return (fromFile == null ? emptySet : fromFile.keySet());
    }
}
