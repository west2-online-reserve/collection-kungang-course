package com.y.schoolhistorymuseum.service;

import com.y.schoolhistorymuseum.mapper.JoinMapper;
import com.y.schoolhistorymuseum.pojo.Exhibit;
import com.y.schoolhistorymuseum.pojo.Exhibition;
import com.y.schoolhistorymuseum.pojo.ExhibitionDetail;
import jakarta.annotation.Resource;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class JoinServiceImpl implements JoinService{

    @Resource
    private JoinMapper joinMapper;

    @Override
    public Exhibition getExhibition(int id) {
        return joinMapper.getExhibition(id);
    }

    @Override
    public List<Exhibit> getExhibits(int id) {
        return joinMapper.getExhibits(id);
    }
}
