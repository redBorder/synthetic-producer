package net.redborder.utils.types.impl;

import com.google.common.net.InetAddresses;
import net.redborder.utils.types.Type;

import java.net.InetAddress;
import java.util.Map;
import java.util.Random;

public class IpType implements Type {
    private Random randomGen = new Random();
    private Integer min, max;

    public IpType(Map<String, Object> params) {
        String minIpStr = (String) params.get("min");
        String maxIpStr = (String) params.get("max");

        if (minIpStr != null) {
            InetAddress minIp = InetAddresses.forString(minIpStr);
            min = InetAddresses.coerceToInteger(minIp);
        } else {
            min = 0;
        }

        if (maxIpStr != null) {
            InetAddress maxIp = InetAddresses.forString(maxIpStr);
            max = InetAddresses.coerceToInteger(maxIp) + 1;
        } else {
            max = Integer.MAX_VALUE;
        }
    }

    @Override
    public Object get() {
        Integer rand = (randomGen.nextInt(max - min) + min);
        return InetAddresses.fromInteger(rand);
    }
}
