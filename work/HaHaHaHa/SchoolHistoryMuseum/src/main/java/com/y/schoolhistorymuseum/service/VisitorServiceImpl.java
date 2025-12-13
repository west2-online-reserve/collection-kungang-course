package com.y.schoolhistorymuseum.service;

import com.baomidou.mybatisplus.extension.service.impl.ServiceImpl;
import com.y.schoolhistorymuseum.mapper.VisitorMapper;
import com.y.schoolhistorymuseum.pojo.Visitor;
import org.springframework.stereotype.Service;

@Service
public class VisitorServiceImpl extends ServiceImpl<VisitorMapper, Visitor> implements VisitorService{
    @Override
    public Visitor getVisitorByVisitorId(Integer visitorId) {
        return baseMapper.selectById(visitorId);
    }

    @Override
    public int saveVisitor(Visitor visitor) {
        return baseMapper.insert(visitor);
    }
}
