package com.y.schoolhistorymuseum.utils;

import com.y.schoolhistorymuseum.pojo.Exhibit;
import com.y.schoolhistorymuseum.pojo.Exhibition;
import jakarta.annotation.Resource;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.redis.core.RedisTemplate;
import org.springframework.stereotype.Component;

import java.util.*;
import java.util.concurrent.TimeUnit;
import java.util.stream.Collectors;

@Component
public class RedisUtil {

    @Autowired
    private RedisTemplate<String, Object> redisTemplate = new RedisTemplate<>();

    /**
     * 将展区信息保存到redis
     * @param constant
     * @param value
     */
    public void saveExhibitionInfo(String constant, Exhibition value){

        String key = constant + ":" +value.getId();
        Map<String, Object> map = new HashMap<>();
        map.put("id", value.getId());
        map.put("title", value.getTitle());
        map.put("bannerUrl", value.getBannerUrl());
        map.put("content", value.getContent());
        redisTemplate.opsForHash().putAll(key, map);
        // 设置过期时间
        redisTemplate.expire(key, 72, TimeUnit.HOURS);
    }

    /**
     * 从redis中获取展区信息
     * @param constant
     * @param id
     */
    public Exhibition getExhibitionInfo(String constant, Integer id){
        String key = constant +":" + id;

        Map<Object, Object> map = redisTemplate.opsForHash().entries(key);
        if (map.isEmpty()){
            return null;
        }
        Exhibition exhibition = new Exhibition();
        exhibition.setId((Integer)map.get("id"));
        exhibition.setTitle((String)map.get("title"));
        exhibition.setBannerUrl((String)map.get("bannerUrl"));
        exhibition.setContent((String)map.get("content"));
        return exhibition;
    }

    /**
     * 将展品信息保存redis中
     * @param constant
     * @param exhibits
     */
    public void saveExhibitInfo(String constant, Set<Object> exhibits){
        List<Exhibit> exhibits1  = exhibits.stream().map(o -> (Exhibit) o).collect(Collectors.toList());
        String key = constant + ":" + exhibits1.get(0).getId();
        redisTemplate.opsForSet().add(key, exhibits);
        // 设置过期时间
        redisTemplate.expire(key, 72, TimeUnit.HOURS);
    }

    /**
     * 从redis中获取展品信息
     * @param constant
     * @param id
     */
    public Set<Object> getExhibitInfo(String constant, Integer id) {
        String key = constant + ":" + id;
        Set<Object> exhibits =  redisTemplate.opsForSet().members(key);
        if (exhibits == null){
            return null;
        }
        return exhibits;
    }

}
