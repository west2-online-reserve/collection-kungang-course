package com.y.schoolhistorymuseum.pojo;

import java.util.List;

public class Result<T> {
    private boolean success; // 接口是否成功
    private T data;          // 成功时返回的数据
    private String message;  // 失败时的提示信息
    private List<Exhibit> exhibits;// 相关展品

    // 成功响应（带数据）
    public static <T> Result<T> success(T data, List<Exhibit> exhibits) {
        Result<T> result = new Result<>();
        result.setSuccess(true);
        result.setData(data);
        result.setMessage("操作成功");
        result.setExhibits(exhibits);
        return result;
    }

    // 失败响应（带提示）
    public static <T> Result<T> fail(String message) {
        Result<T> result = new Result<>();
        result.setSuccess(false);
        result.setMessage(message);
        return result;
    }

    // 失败响应（默认提示）
    public static <T> Result<T> fail() {
        return fail("暂无相关数据");
    }

    // Getter + Setter
    public boolean isSuccess() {
        return success;
    }

    public void setSuccess(boolean success) {
        this.success = success;
    }

    public T getData() {
        return data;
    }

    public void setData(T data) {
        this.data = data;
    }

    public String getMessage() {
        return message;
    }

    public void setMessage(String message) {
        this.message = message;
    }

    public List<Exhibit> getExhibits() {
        return exhibits;
    }

    public void setExhibits(List<Exhibit> exhibits) {
        this.exhibits = exhibits;
    }
}
