package com.y.schoolhistorymuseum.pojo;

import java.io.Serializable;

public class Exhibit implements Serializable {
    private Integer id;

    private String name;

    private String imageUrl;

    private String desc;

    public Exhibit(Integer id, String name, String imageUrl, String desc) {
        this.id = id;
        this.name = name;
        this.imageUrl = imageUrl;
        this.desc = desc;
    }

    public Exhibit() {
    }

    public Integer getId() {
        return id;
    }

    public void setId(Integer id) {
        this.id = id;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public String getImageUrl() {
        return imageUrl;
    }

    public void setImageUrl(String imageUrl) {
        this.imageUrl = imageUrl;
    }

    public String getDesc() {
        return desc;
    }

    public void setDesc(String desc) {
        this.desc = desc;
    }

    @Override
    public String toString() {
        return "Exhibit{" +
                "id=" + id +
                ", name='" + name + '\'' +
                ", imageUrl='" + imageUrl + '\'' +
                ", desc='" + desc + '\'' +
                '}';
    }
}
