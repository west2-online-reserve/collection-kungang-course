package com.y.schoolhistorymuseum.service;

import com.baomidou.mybatisplus.extension.service.IService;
import com.y.schoolhistorymuseum.pojo.Visitor;

public interface VisitorService extends IService<Visitor> {
    /**
     *  根据参观id查找该预约的相关信息
     * @param visitorId
     * @return
     */
    Visitor getVisitorByVisitorId(Integer visitorId);

    /**
     *  登记预约的信息
     * @param visitor
     */
    int saveVisitor(Visitor visitor);

}
