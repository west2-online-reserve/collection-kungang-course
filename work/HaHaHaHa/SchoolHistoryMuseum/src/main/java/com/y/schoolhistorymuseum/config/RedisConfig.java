package com.y.schoolhistorymuseum.config;

import com.fasterxml.jackson.annotation.JsonAutoDetect;
import com.fasterxml.jackson.annotation.PropertyAccessor;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.jsontype.impl.LaissezFaireSubTypeValidator;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.data.redis.connection.RedisConnectionFactory;
import org.springframework.data.redis.core.RedisTemplate;
import org.springframework.data.redis.serializer.Jackson2JsonRedisSerializer;
import org.springframework.data.redis.serializer.StringRedisSerializer;

@Configuration
public class RedisConfig {

    @Bean
    public RedisTemplate<String, Object> redisTemplate(RedisConnectionFactory factory) {
        RedisTemplate<String, Object> template = new RedisTemplate<>();
        template.setConnectionFactory(factory);

        // 1. 创建ObjectMapper并配置，负责java对象和json字符串的转换
        ObjectMapper mapper = new ObjectMapper();
        // 允许访问所有字段（包括私有字段）
        mapper.setVisibility(PropertyAccessor.ALL, JsonAutoDetect.Visibility.ANY);
        // 启用默认类型（解决反序列化时的类型识别问题）
        mapper.activateDefaultTyping(LaissezFaireSubTypeValidator.instance,
                ObjectMapper.DefaultTyping.NON_FINAL);

        // 2. 通过构造函数传入ObjectMapper（替代setObjectMapper()）
        Jackson2JsonRedisSerializer<Object> serializer = new Jackson2JsonRedisSerializer<>(mapper, Object.class);

        // 3. 配置序列化器
        StringRedisSerializer stringSerializer = new StringRedisSerializer();
        template.setKeySerializer(stringSerializer);       // key用String序列化
        template.setValueSerializer(serializer);           // value用JSON序列化
        template.setHashKeySerializer(stringSerializer);   // hash的key也用String序列化
        template.setHashValueSerializer(serializer);       // hash的value用JSON序列化
        //完成初始化
        template.afterPropertiesSet();

        return template;
    }
}
