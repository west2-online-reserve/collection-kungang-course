package com.y.schoolhistorymuseum.mapper;

import com.y.schoolhistorymuseum.pojo.Exhibit;
import com.y.schoolhistorymuseum.pojo.Exhibition;
import com.y.schoolhistorymuseum.pojo.ExhibitionDetail;
import org.apache.ibatis.annotations.Mapper;
import org.springframework.stereotype.Repository;

import java.util.List;

@Mapper
@Repository
public interface JoinMapper {

    // 获取展区信息
    Exhibition getExhibition(int id);

    // 获取展区展品信息
    List<Exhibit> getExhibits(int id);
}
