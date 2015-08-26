package net.redborder.utils.generators.types;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.util.Map;
import java.util.Random;

public class MacType implements Type {
    private final static Logger log = LoggerFactory.getLogger(MacType.class);

    private Random randomGen = new Random();
    private Long min, max;

    public MacType(Map<String, Object> params) {
        String minMacStr = (String) params.get("min");
        String maxMacStr = (String) params.get("max");

        if (minMacStr != null) {
            min = longFromMac(minMacStr);
        } else {
            min = 0L;
        }

        if (maxMacStr != null) {
            max = longFromMac(maxMacStr);
        } else {
            max = Long.MAX_VALUE;
        }
    }

    @Override
    public Object get() {
        long rand = (long) (randomGen.nextDouble() * (max - min));
        long selectedMac = min + rand;
        return macFromLong(selectedMac);
    }

    public static String macFromLong(long address) {
        StringBuilder builder = new StringBuilder();

        byte[] addressInBytes = new byte[] {
                (byte)((address >> 40) & 0xff),
                (byte)((address >> 32) & 0xff),
                (byte)((address >> 24) & 0xff),
                (byte)((address >> 16) & 0xff),
                (byte)((address >> 8 ) & 0xff),
                (byte)(address & 0xff)
        };

        for (byte b: addressInBytes) {
            if (builder.length() > 0) {
                builder.append(":");
            }
            builder.append(String.format("%02X", b & 0xFF));
        }

        return builder.toString();
    }

    public static long longFromMac(String address) {
        String[] elements = address.split(":");
        byte[] addressInBytes = new byte[6];
        long mac = 0;

        for (int i = 0; i < 6; i++) {
            String element = elements[i];
            addressInBytes[i] = (byte) Integer.parseInt(element, 16);
        }

        for (int i = 0; i < 6; i++) {
            long t = (addressInBytes[i] & 0xffL) << ((5 - i) * 8);
            mac |= t;
        }

        return mac;
    }
}
