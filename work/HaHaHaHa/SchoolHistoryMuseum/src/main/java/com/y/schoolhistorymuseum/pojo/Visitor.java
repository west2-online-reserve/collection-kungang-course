package com.y.schoolhistorymuseum.pojo;

import com.baomidou.mybatisplus.annotation.TableField;
import com.baomidou.mybatisplus.annotation.TableName;

import java.time.LocalDate;
import java.time.LocalDateTime;

@TableName("visitors")
public class Visitor {

    // 数据库中的编号
    private int id;

    // 联系人姓名
    @TableField("contact_name")
    private String contactName;

    // 联系人电话
    @TableField("telephone_number")
    private String telephoneNumber;

    // 单位/团体名称
    @TableField("group_name")
    private String groupName;

    @TableField("number")
    // 预约人数
    private int number;

    @TableField("date")
    // 预约时间的日期
    private LocalDate date;

    @TableField("time")
    // 预约时间段
    private String time;

    public Visitor() {}

    public Visitor(int id, String contactName, String telephoneNumber, String groupName, int number, LocalDate date, String time) {
        this.id = id;
        this.contactName = contactName;
        this.telephoneNumber = telephoneNumber;
        this.groupName = groupName;
        this.number = number;
        this.date = date;
        this.time = time;
    }

    public Visitor(String contactName, String telephoneNumber, String groupName, int number, LocalDate date, String time) {
        this.contactName = contactName;
        this.telephoneNumber = telephoneNumber;
        this.groupName = groupName;
        this.number = number;
        this.date = date;
        this.time = time;
    }

    public String getContactName() {
        return contactName;
    }

    public int getId() {
        return id;
    }

    public void setId(int id) {
        this.id = id;
    }

    public void setContactName(String contactName) {
        this.contactName = contactName;
    }

    public String getTelephoneNumber() {
        return telephoneNumber;
    }

    public void setTelephoneNumber(String telephoneNumber) {
        this.telephoneNumber = telephoneNumber;
    }

    public String getGroupName() {
        return groupName;
    }

    public void setGroupName(String groupName) {
        this.groupName = groupName;
    }

    public int getNumber() {
        return number;
    }

    public void setNumber(int number) {
        this.number = number;
    }

    public LocalDate getDate() {
        return date;
    }

    public void setDate(LocalDate date) {
        this.date = date;
    }

    public String getTime() {
        return time;
    }

    public void setTime(String time) {
        this.time = time;
    }
}
