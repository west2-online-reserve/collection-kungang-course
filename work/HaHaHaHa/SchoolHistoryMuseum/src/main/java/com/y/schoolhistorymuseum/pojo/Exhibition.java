package com.y.schoolhistorymuseum.pojo;

import com.baomidou.mybatisplus.annotation.TableField;
import com.baomidou.mybatisplus.annotation.TableName;

@TableName("exhibition_detail")
public class Exhibition {

    @TableField("title")
    private String title;

    @TableField("id")
    private Integer id;

    @TableField("banner_url")
    private String bannerUrl;

    @TableField("content")
    private String content;

    public Exhibition() {
    }

    public String getTitle() {
        return title;
    }

    public void setTitle(String title) {
        this.title = title;
    }

    public Integer getId() {
        return id;
    }

    public void setId(Integer id) {
        this.id = id;
    }

    public String getBannerUrl() {
        return bannerUrl;
    }

    public void setBannerUrl(String bannerUrl) {
        this.bannerUrl = bannerUrl;
    }

    public String getContent() {
        return content;
    }

    public void setContent(String content) {
        this.content = content;
    }

    @Override
    public String toString() {
        return "Exhibition{" +
                "title='" + title + '\'' +
                ", id=" + id +
                ", bannerUrl='" + bannerUrl + '\'' +
                ", content='" + content + '\'' +
                '}';
    }
}
