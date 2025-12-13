package com.y.schoolhistorymuseum.mapper;

import com.baomidou.mybatisplus.core.mapper.BaseMapper;
import com.y.schoolhistorymuseum.pojo.Visitor;
import org.apache.ibatis.annotations.Mapper;
import org.springframework.stereotype.Repository;

@Mapper
@Repository
public interface VisitorMapper extends BaseMapper<Visitor> {
}
