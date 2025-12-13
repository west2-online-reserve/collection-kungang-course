package com.y.schoolhistorymuseum.controller;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.y.schoolhistorymuseum.pojo.*;
import com.y.schoolhistorymuseum.service.JoinServiceImpl;
import com.y.schoolhistorymuseum.service.VisitorServiceImpl;
import com.y.schoolhistorymuseum.utils.RedisUtil;
import constant.RedisKeys;
import jakarta.annotation.Resource;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.*;

import java.time.LocalDate;
import java.time.LocalDateTime;
import java.util.*;
import java.util.stream.Collectors;

@Controller
@RequestMapping("/Fzu")
public class ShowController {

    @Resource
    private JoinServiceImpl joinService;

    @Resource
    private VisitorServiceImpl visitorService;

    @Resource
    private RedisUtil redisUtil;


    @GetMapping("/school_history_museum")
    public String show(Model model){
        return "SchoolHistoryMuseum";
    }

    // 模拟数据库：初始化6个展区的完整数据
//    private final List<ExhibitionDetail> exhibitionData = new ArrayList<>();

//    // 初始化所有展区数据（1-6号展区完整实现）
//    private List<ExhibitionDetail> initAllExhibitionData() {
//        List<ExhibitionDetail> allExhibits = new ArrayList<>();
//
//        // 1. 历史沿革展区（id=1）
//        List<Exhibit> exhibits1 = new ArrayList<>();
//        exhibits1.add(new Exhibit(101, "1958年建校文件", "https://picsum.photos/id/28/300/200", "记录学校创建的原始档案，含国务院批文"));
//        exhibits1.add(new Exhibit(102, "早期校园地图", "https://picsum.photos/id/29/300/200", "1960年代校园布局图，标注初代教学楼位置"));
//        exhibits1.add(new Exhibit(103, "建校周年纪念章", "https://picsum.photos/id/30/300/200", "1988年建校30周年纪念徽章"));
//        allExhibits.add(new ExhibitionDetail(
//                1,
//                "历史沿革展区",
//                "https://picsum.photos/id/28/1200/600",
//                "<p class='mb-4'>本展区系统展示了学校从1958年建校至今的发展历程，分为四个关键阶段：</p>" +
//                        "<p class='mb-2'>1. <strong>初创时期（1958-1978）</strong>：依托厦门大学建立，奠定工科基础，开设机械、化工等核心专业；</p>" +
//                        "<p class='mb-2'>2. <strong>发展时期（1978-1996）</strong>：恢复高考后扩大招生规模，学科体系逐步完善，新增计算机、自动化等专业；</p>" +
//                        "<p class='mb-2'>3. <strong>跃升时期（1996-2010）</strong>：成功进入国家“211工程”重点建设高校行列，科研实力显著提升；</p>" +
//                        "<p>4. <strong>腾飞时期（2010至今）</strong>：入选国家“双一流”建设高校，聚焦世界一流学科建设，迈向高水平研究型大学。</p>",
//                exhibits1
//        ));
//
//        // 2. 名师风采展区（id=2）
//        List<Exhibit> exhibits2 = new ArrayList<>();
//        exhibits2.add(new Exhibit(201, "卢嘉锡院士手稿", "https://picsum.photos/id/48/300/200", "著名化学家、教育家的科研笔记，记录催化反应研究思路"));
//        exhibits2.add(new Exhibit(202, "付贤智院士获奖证书", "https://picsum.photos/id/49/300/200", "2009年国家技术发明奖一等奖证书"));
//        exhibits2.add(new Exhibit(203, "教学名师荣誉勋章", "https://picsum.photos/id/50/300/200", "王晨教授获“国家级教学名师”称号的荣誉勋章"));
//        allExhibits.add(new ExhibitionDetail(
//                2,
//                "名师风采展区",
//                "https://picsum.photos/id/48/1200/600",
//                "<p class='mb-4'>本展区集中展示学校历代名师的学术成就与育人风采，涵盖两院院士、国家级教学名师等杰出代表：</p>" +
//                        "<p class='mb-2'>1. <strong>两院院士</strong>：卢嘉锡、付贤智等在化学、材料科学领域的突出贡献，推动国家科研进步；</p>" +
//                        "<p class='mb-2'>2. <strong>国家级教学名师</strong>：王晨、李刚等教授在教育改革中的创新实践，编写国家级规划教材；</p>" +
//                        "<p class='mb-2'>3. <strong>青年拔尖人才</strong>：近五年入选“长江学者奖励计划”“国家优青”的青年教师代表；</p>" +
//                        "<p>4. <strong>师德标兵</strong>：深耕教学一线、深受学生爱戴的优秀教师典型案例。</p>",
//                exhibits2
//        ));
//
//        // 3. 教学科研展区（id=3）
//        List<Exhibit> exhibits3 = new ArrayList<>();
//        exhibits3.add(new Exhibit(301, "国家科技进步奖证书", "https://picsum.photos/id/60/300/200", "2023年“新型半导体材料制备技术”获国家科技进步二等奖"));
//        exhibits3.add(new Exhibit(302, "ESI学科排名证书", "https://picsum.photos/id/61/300/200", "12个学科进入ESI全球前1%的官方认证"));
//        exhibits3.add(new Exhibit(303, "国家重点实验室牌匾", "https://picsum.photos/id/62/300/200", "“光催化国家重点实验室”授牌仪式纪念"));
//        allExhibits.add(new ExhibitionDetail(
//                3,
//                "教学科研展区",
//                "https://picsum.photos/id/60/1200/600",
//                "<p class='mb-4'>本展区全面展示学校在教学改革与科研创新领域的核心成果：</p>" +
//                        "<p class='mb-2'>1. <strong>学科建设</strong>：12个ESI学科进入全球前1%，其中化学、材料科学进入前1‰；</p>" +
//                        "<p class='mb-2'>2. <strong>科研平台</strong>：拥有国家重点实验室3个、省部级科研平台28个，科研设备总值超20亿元；</p>" +
//                        "<p class='mb-2'>3. <strong>重大成果</strong>：近五年获国家科技奖8项，承担国家级科研项目1200余项，发表SCI论文1.5万余篇；</p>" +
//                        "<p>4. <strong>教学改革</strong>：国家级一流本科专业建设点45个，虚拟仿真实验教学中心3个，培养各类人才超30万名。</p>",
//                exhibits3
//        ));
//
//        // 4. 校园文化展区（id=4）
//        List<Exhibit> exhibits4 = new ArrayList<>();
//        exhibits4.add(new Exhibit(401, "校徽校旗实物", "https://picsum.photos/id/70/300/200", "1958年原版校徽与2018年修订版校旗"));
//        exhibits4.add(new Exhibit(402, "校训石拓片", "https://picsum.photos/id/71/300/200", "“明德至诚，博学远志”校训石的拓印作品"));
//        exhibits4.add(new Exhibit(403, "校园文化节纪念册", "https://picsum.photos/id/72/300/200", "连续20届校园文化节的活动集锦与纪念品"));
//        allExhibits.add(new ExhibitionDetail(
//                4,
//                "校园文化展区",
//                "https://picsum.photos/id/70/1200/600",
//                "<p class='mb-4'>本展区呈现学校独特的校园文化与精神传承：</p>" +
//                        "<p class='mb-2'>1. <strong>精神内核</strong>：“明德至诚，博学远志”的校训，“团结、勤奋、严谨、创新”的校风；</p>" +
//                        "<p class='mb-2'>2. <strong>文化符号</strong>：校徽、校旗、校歌的设计理念与历史演变，标志性建筑（如图书馆、校训石）的文化内涵；</p>" +
//                        "<p class='mb-2'>3. <strong>品牌活动</strong>：校园文化节、科技艺术节、辩论赛、志愿服务等特色活动，年均开展各类文化活动500余场；</p>" +
//                        "<p>4. <strong>学生社团</strong>：120余个学生社团，涵盖学术科技、文艺体育、公益服务等领域，丰富学生课余生活。</p>",
//                exhibits4
//        ));
//
//        // 5. 校友成就展区（id=5）
//        List<Exhibit> exhibits5 = new ArrayList<>();
//        exhibits5.add(new Exhibit(501, "校友企业家荣誉墙", "https://picsum.photos/id/80/300/200", "福布斯中国富豪榜入选校友的创业故事"));
//        exhibits5.add(new Exhibit(502, "学术领域杰出校友证书", "https://picsum.photos/id/81/300/200", "当选两院院士、长江学者的校友荣誉证明"));
//        exhibits5.add(new Exhibit(503, "校友捐赠纪念物", "https://picsum.photos/id/82/300/200", "校友捐赠的教学楼模型、奖学金纪念牌"));
//        allExhibits.add(new ExhibitionDetail(
//                5,
//                "校友成就展区",
//                "https://picsum.photos/id/80/1200/600",
//                "<p class='mb-4'>本展区展示海内外校友在各领域的卓越成就与社会贡献：</p>" +
//                        "<p class='mb-2'>1. <strong>商界精英</strong>：培养了一大批上市公司创始人、行业领军企业家，校友企业年营收超万亿；</p>" +
//                        "<p class='mb-2'>2. <strong>学术翘楚</strong>：近200名校友当选两院院士、国家级人才计划入选者，在科研领域发光发热；</p>" +
//                        "<p class='mb-2'>3. <strong>政界栋梁</strong>：多名校友担任省部级领导职务，为国家治理与地方发展贡献力量；</p>" +
//                        "<p>4. <strong>社会楷模</strong>：在公益慈善、应急救援、基层服务等领域涌现的校友先进典型。</p>",
//                exhibits5
//        ));
//
//        // 6. 互动体验展区（id=6）
//        List<Exhibit> exhibits6 = new ArrayList<>();
//        exhibits6.add(new Exhibit(601, "VR校园漫游设备", "https://picsum.photos/id/90/300/200", "沉浸式体验校园全景，支持历史场景还原"));
//        exhibits6.add(new Exhibit(602, "校史知识问答终端", "https://picsum.photos/id/91/300/200", "互动答题赢取纪念品，普及校史知识"));
//        exhibits6.add(new Exhibit(603, "校友留言墙系统", "https://picsum.photos/id/92/300/200", "扫码留下祝福，查看全球校友留言"));
//        allExhibits.add(new ExhibitionDetail(
//                6,
//                "互动体验展区",
//                "https://picsum.photos/id/90/1200/600",
//                "<p class='mb-4'>本展区通过科技手段打造沉浸式互动体验，让参观者深度参与：</p>" +
//                        "<p class='mb-2'>1. <strong>VR校园漫游</strong>：佩戴VR设备，“穿越”不同历史时期的校园，感受学校变迁；</p>" +
//                        "<p class='mb-2'>2. <strong>校史知识问答</strong>：触摸终端参与答题，涵盖校史、学科、名师等知识点，答题满分可获得定制纪念品；</p>" +
//                        "<p class='mb-2'>3. <strong>校友留言墙</strong>：扫码登录后留下参观感悟或对学校的祝福，留言将同步展示在实体留言墙与线上平台；</p>" +
//                        "<p>4. <strong>科研成果互动演示</strong>：通过模型与动画演示学校重大科研成果的原理与应用场景。</p>",
//                exhibits6
//        ));
//
//        return allExhibits;
//    }

    // 详情接口：接收前端id参数，返回对应展区数据
    @GetMapping("/detail")
    @ResponseBody
    public Result<ExhibitionDetail> getExhibitionDetail(@RequestParam("id") Integer id) {
        // 校验id合法性（1-6）
        if (id == null || id < 1 || id > 6) {
            return Result.fail("无效的展区ID");
        }
        Exhibition exhibition = new Exhibition();
        Set<Object> exhibits;
        List<Exhibit> exhibits1 = new ArrayList<>();

        // 从redis中获取
        exhibition = redisUtil.getExhibitionInfo(RedisKeys.exhibitionsKey, id);
        exhibits = redisUtil.getExhibitInfo(RedisKeys.exhibitsKey, id);


        // 如果redis中没有，则从数据库中获取
        if (exhibition == null) {
            exhibition = joinService.getExhibition(id);
            redisUtil.saveExhibitionInfo(RedisKeys.exhibitionsKey, exhibition);
        }
        if (exhibits.isEmpty()) {
            exhibits1 = joinService.getExhibits(id);
            exhibits = exhibits1.stream().map(o -> (Object)o).collect(Collectors.toSet());
            redisUtil.saveExhibitInfo(RedisKeys.exhibitsKey, exhibits);
        } else {
            exhibits1 = joinService.getExhibits(id);
        }
        ExhibitionDetail exhibitionDetail = new ExhibitionDetail(exhibition, exhibits1);

        return Result.success(exhibitionDetail, exhibits1); // 成功返回数据
    }

    @GetMapping("/detail.html")
    public String detail(){
        return "detail";
    }

    /**
     * 提交预约信息到mysql
     */
    @PostMapping("/submit")
    @ResponseBody
    Map<String, Object> submit(@RequestBody Map<String, Object> map){
        Map<String, Object> result = new HashMap<>();

        try {
            LocalDate date = LocalDate.parse(map.get("date").toString());
            Visitor visitor = new Visitor(map.get("name").toString(), map.get("phone").toString(), map.get("organization").toString(), Integer.parseInt((String) map.get("number")), date, map.get("time").toString());
            visitorService.saveVisitor(visitor);
            result.put("date",visitor);
            result.put("success",true);
            result.put("message","预约成功！");
            return result;
        } catch (Exception e){
            e.printStackTrace();
            result.put("message","预约失败！" + e.getMessage());
            result.put("success",false);
            return result;
        }
    }

    @GetMapping("/carousel")
    public String carousel(){
        return "carousel";
    }
}
