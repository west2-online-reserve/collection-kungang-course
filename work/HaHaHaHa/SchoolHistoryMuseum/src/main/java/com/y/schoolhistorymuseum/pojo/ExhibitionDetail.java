package com.y.schoolhistorymuseum.pojo;


import java.util.List;

public class ExhibitionDetail {

    private String title;

    private Integer id;

    private String bannerUrl;

    private String content;

    private List<Exhibit> exhibits;



    public ExhibitionDetail(Integer id, String title, String bannerUrl, String content, List<Exhibit> exhibits) {
        this.title = title;
        this.id = id;
        this.bannerUrl = bannerUrl;
        this.content = content;
        this.exhibits = exhibits;
    }

    public ExhibitionDetail(Exhibition exhibition, List<Exhibit> exhibits) {
        this.title = exhibition.getTitle();
        this.id = exhibition.getId();
        this.bannerUrl = exhibition.getBannerUrl();
        this.content = exhibition.getContent();
        this.exhibits = exhibits;
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

    public List<Exhibit> getExhibits() {
        return exhibits;
    }

    public void setExhibits(List<Exhibit> exhibits) {
        this.exhibits = exhibits;
    }
}
