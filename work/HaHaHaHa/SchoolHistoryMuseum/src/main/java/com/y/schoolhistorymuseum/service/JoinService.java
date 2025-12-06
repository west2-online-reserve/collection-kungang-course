package com.y.schoolhistorymuseum.service;


import com.y.schoolhistorymuseum.pojo.Exhibit;
import com.y.schoolhistorymuseum.pojo.Exhibition;
import com.y.schoolhistorymuseum.pojo.ExhibitionDetail;

import java.util.List;

public interface JoinService {

    // 获取展区信息
    Exhibition getExhibition(int id);

    // 获取展区展品信息
    List<Exhibit> getExhibits(int id);
}
