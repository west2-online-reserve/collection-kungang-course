// types/nav.ts
export interface NavItem {
  id: string | number
  name: string
  page: string
}

export interface UserData {
  name: string
}

// 定义导航栏的Props接口
export interface NavBarProps {
  navItems: NavItem[]
  user: UserData
  currentPage: string
}