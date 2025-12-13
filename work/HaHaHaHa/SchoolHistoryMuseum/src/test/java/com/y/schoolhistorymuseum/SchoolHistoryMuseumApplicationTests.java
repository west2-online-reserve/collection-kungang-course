package com.y.schoolhistorymuseum;


import com.y.schoolhistorymuseum.mapper.JoinMapper;
import com.y.schoolhistorymuseum.pojo.Exhibit;
import com.y.schoolhistorymuseum.pojo.Exhibition;
import com.y.schoolhistorymuseum.pojo.ExhibitionDetail;
import com.y.schoolhistorymuseum.utils.RedisUtil;
import constant.RedisKeys;
import jakarta.annotation.Resource;
import org.junit.jupiter.api.Test;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.data.redis.core.RedisTemplate;

import java.time.LocalDateTime;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Set;

import static org.junit.jupiter.api.Assertions.assertEquals;

@SpringBootTest
class SchoolHistoryMuseumApplicationTests {

    @Resource
    private RedisTemplate<Object, Object> redisTemplate;

    @Resource
    private JoinMapper joinMapper;

    @Resource
    private RedisUtil redisUtil;

    @Test
    void contextLoads() {
        LocalDateTime time = LocalDateTime.now();
        System.out.println(time);
    }

    @Test
    void test() {
        Exhibition exhibition = joinMapper.getExhibition(1);
        System.out.println(exhibition);
    }


    @Test
    public void testHashOperations() {
        Map<String, Object> map = new HashMap<>();
        map.put("field1", "value1");
        map.put("field2", "value2");

        redisTemplate.opsForHash().putAll("test:hash", map);
        Map<Object, Object> result = redisTemplate.opsForHash().entries("test:hash");
        assertEquals(2, result.size());
    }

    @Test
    void test2(){
        Set<Object> exhibitSet = redisUtil.getExhibitInfo(RedisKeys.exhibitsKey,2);
        for (Object o : exhibitSet){
            System.out.println(o);
        }
    }

}
