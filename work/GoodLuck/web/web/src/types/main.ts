
//子组件props管理
interface MdOptions {
    html: boolean, // 启用HTML标签
    linkify: boolean, // 自动链接识别
    typographer: boolean, // 印刷样式优化
    breaks: boolean, // 换行转换为<br>
}

export interface HomeProps {
    options?: MdOptions
    username: string

}
export interface HistoryProps{
  //
  unk?:unknown

}
export interface TrainProps{
  //
  unk?:unknown
}

export interface ComponentPropsMap {
  home: HomeProps
  history: HistoryProps
  train:TrainProps

}

// 组件名称类型
export type ComponentName = keyof ComponentPropsMap
